from labylib import Cape
from threading import Thread, Event
from pathlib import Path

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import platform
import getpass
import subprocess

# Chattycape daemon
class Chattycape(Thread):

	pollRate = 1 # Logfile pollrate
	updateRate = 1 # Update rate of Labylib cosmetic

	def __init__(self,event,phpsessid,logfile):
		Thread.__init__(self)
		self.stopped = event

		self.phpsessid = phpsessid
		self.logfile = logfile

		self.line = ""

		self.i = 0

	# Poll last line from logfile
	def linefeed(self):
		self.line = subprocess.check_output(['tail','-1',self.logfile])

	# Update labylib cosmetic
	def update(self):
		print(self.line)

	def run(self):
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
		self.phpsessid = input("\nhttps://github.com/VictorWesterlund/labylib#find-your-phpsessid-cookie\nPaste your PHPSESSID here:\n")

		self.start()

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

		path = input("Please paste the path to your '.minecraft'-folder:\n")
		
		if(Path(path).exists()):
			return path + mclog

		print(f"\nInvalid path; No Minecraft-installation found at '{path}'")
		self.locate()

	def start(self):
		stop = Event()

		# Start the daemon
		chattycape = Chattycape(stop,self.phpsessid,self.logfile)
		chattycape.start()

		interrupt = input("\nRunning! Press enter to stop\n")
		stop.set() # Stop the daemon
		print("Bye!")

main = Main()
print(main.file)