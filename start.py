from labylib import Cape
from threading import Thread, Event
from pathlib import Path

import re
import json
import platform
import getpass
import subprocess
import requests

# Chattycape daemon
class Chattycape(Thread):

	pollRate = 1 # Logfile pollrate
	updateRate = 1 # Update rate of Labylib cosmetic

	def __init__(self,event,phpsessid,endpoint,logfile,me = "None"):
		Thread.__init__(self)
		self.stopped = event
		self.params = (phpsessid,endpoint,logfile,me) # Create tuple from params

		self.server = None # Connected to server (hostname)
		self.config = None # Chat config for current server

		self.line = "[21:42:25] [main/INFO]: [CHAT] 725 IMMORTAL VicW test"
		self.i = 0

	# Read last line from logfile
	def linefeed(self):
		# tail last line from logfile
		line = subprocess.check_output(['tail','-1',self.params[2]]).decode("utf-8","ignore")[:-2]

		match = re.search(self.config["pattern"],line)

		if match:
			self.line = line
			return

	# Extract Minecraft username and tag from current line
	def getUser(self):
		line = self.line[31:].split() # Split current line. Offset (31) for log-prefixes

		username = tag = "None"

		start = self.config["lookup"]["start"] # List offset for iterator
		ignoreList = self.config["lookup"]["ignore"] # Jumps to next index if match
		tagList = self.config["lookup"]["tag"] # 'tag' set if match

		for substr in line[start:]: # Start at offset
			if substr in ignoreList:
				continue
			
			if substr in tagList:
				tag = substr
				continue
			
			# Not ignored, and not a tag, so assume we've reached the username
			username = substr
			break

		return (username,tag)

	# Update labylib cosmetic
	def update(self):
		args = self.getUser() # Get minecraft username and tag

		urlparams = f"?server={self.server}&ign={args[0]}&rank={args[1]}"

		# Save cape texture from endpoint to disk
		with open(".cache.png","wb") as handle:
			fetch = requests.get(self.params[1] + urlparams,stream=True)

			if not fetch.ok:
				print(fetch)

			for block in fetch.iter_content(1024):
				if not block:
					break

				handle.write(block)
		
		# TODO: Labylib here

	# ----------------------------

	# Import RegEx patterns for current server
	def loadConfig(self):
		self.server = "us.mineplex.com"

		with open("./servers.json") as config:
			data = json.load(config)

		self.config = data[self.server]
		self.config["pattern"] = r"\[CHAT\]+ " + self.config["pattern"]

	# Start the thread
	def run(self):
		print("\nRunning..")
		self.loadConfig()

		# Start the chat 'listener'
		while not self.stopped.wait(Chattycape.pollRate):
			self.linefeed() # Poll logfile

			# Cooldown for labylib texture update
			if(self.i >= (Chattycape.updateRate * Chattycape.pollRate)):
				self.update()
				self.i = 0

			self.i += 1


# Initializer and watchdog
class Main:

	def __init__(self):
		print("-- Labylib Chattycape --")
		self.logfile = self.locate()

		self.endpoint = self.prompt("Cape render endpoint","http://192.168.86.21/victor-westerlund/labylib-chattycape/back-end/render.php")
		self.me = self.prompt("My Minecraft in-game name (Case Sensitive)","Don't exclude me")
		self.phpsessid = self.prompt("PHPSESSID cookie")

		self.start()

	# Prompt user to enter information
	def prompt(self,message,default = "None"):
		# Add '[default]' flag if present
		if(default != "None"):
			message += f" [{default}]"
		message += ":"

		value = default
		userinput = input(message + "\n")

		if(userinput):
			value = userinput
			
		return value

	# Attempt to locate '.minecraft' automatically, otherwise prompt user
	def locate(self):
		sys = platform.system() # Get operating system
		user = getpass.getuser() # Get current user

		mclog = "/logs/latest.log"

		# Default locations for various systems
		paths = {
			"Linux": [
				"~/.minecraft",
				f"/mnt/c/Users/{user}/AppData/Roaming/.minecraft", # Windows Subsystem for Linux (WSL)
				f"/home/{user}/.minecraft"
			],
			"Windows": [
				"%APPDATA%\.minecraft",
				f"C://Users/{user}/AppData/Roaming/.minecraft",
			],
			"Darwin": [ 
				"~/Library/Application Support/minecraft" # macOS
			]
		}

		for path in paths[sys]:
			if(Path(path).exists()):
				return path + mclog

		# Failed to locate Minecraft-installation automatically

		path = self.prompt("Path to your '.minecraft'-folder","/mnt/c/Users/victo/AppData/Roaming/.minecraft")
		
		if(Path(path).exists()):
			return path + mclog

		print(f"\nInvalid path; No Minecraft-installation found at '{path}'")
		self.locate()

	def start(self):
		stop = Event()

		# Start the daemon
		chattycape = Chattycape(stop,self.phpsessid,self.endpoint,self.logfile,self.me)
		chattycape.start()

		input("Press enter to stop the daemon")
		stop.set() # Stop the daemon
		print("Stopped!")

Main()