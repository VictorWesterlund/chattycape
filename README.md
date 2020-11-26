![Chattycape Demo](https://storage.googleapis.com/public.victorwesterlund.com/github/VictorWesterlund/chattycape/Capture3.PNG)

# Chattycape

This labylib extension updates your LabyMod cape with tags from Minecraft chat.

* [Get Started](#get-started)
* [Default Behavior](#default-behavior)
* [Custom Render Endpoint](#custom-render-endpoint)
* [Contribute](#contribute)

### [List of supported servers OOTB](https://github.com/VictorWesterlund/chattycape/wiki/Default-endpoint:-Supported-servers)

## Get Started

### IMPORTANT:
Chattycape **overwrites your current LabyMod cape**; so make sure to save it before you begin.

1. Login and open the [LabyMod Dashboard](https://www.labymod.net/dashboard)
2. Under the "YOUR COSMETICS" section, click the tiny image of your cape<br>
![Step 1](https://storage.googleapis.com/public.victorwesterlund.com/github/VictorWesterlund/chattycape/step1.PNG)
3. Right-click the image and select "Save image as.."<br>
*It's called the same in other major browsers. (Screenshot of Chrome)*
![Step 2](https://storage.googleapis.com/public.victorwesterlund.com/github/VictorWesterlund/chattycape/step2.PNG)

### Installation

1. [Download the latest version of Chattycape](https://github.com/VictorWesterlund/chattycape/releases)
2. Download and install the latest version of [Python 3](https://www.python.org/downloads/) for your architecture
3. Install [`labylib`](https://pypi.org/project/labylib/) with [`pip`](https://pip.pypa.io/en/stable/)
```bash
$ python3 -m pip install labylib
```
*or if that doesn't work..*
```bash
$ pip3 install labylib
```

### Usage

1. Run `start.py` with `python3` (not as root)
```bash
$ python3 start.py
```
2. Chattycape CLI will now ask you to provide additonal details.

*and here's an explanation of them all in order:*
| Input | Description |
|--|--|
| `Path to your '.minecraft'-folder:` | _Only appears if your Minecraft-installation couldn't be located automatically._<br>Enter a full (absolute) path to your `.minecraft`-folder. Example: "C://Users/VicW/AppData/Roaming/.minecraft"
| `Cape render endpoint [https://api.victorwesterlund.com/chattycape]:` | Paste a custom render enpoint URL here, or press enter to use the default.
| `My Minecraft in-game name (Case Sensitive) [Don't exclude me]:` | Enter your Minecraft IGN to exclude yourself from tagging or press enter to allow messages from yourself
| `PHPSESSID cookie:` | [Here's what it is and where to find it](https://github.com/VictorWesterlund/labylib/wiki/Find-your-PHPSESSID)

3. That's it. You should now see this at the end of your terminal:<br>
![Terminal](https://storage.googleapis.com/public.victorwesterlund.com/github/VictorWesterlund/chattycape/terminal.PNG)

4. *When you want exit:* Press <kbd>⏎ Enter</kbd> / <kbd>⏎ Return</kbd> to close

## Default Behavior

### [List of supported servers OOTB](https://github.com/VictorWesterlund/chattycape/wiki/Default-endpoint:-Supported-servers)

If you start Chattycape with the default render endpoint; `https://api.victorwesterlund.com/chattycape` - your cape will update every **15 seconds** (limit) with a graphic of the player **avatar, name and tag** (usually "rank") who last said something in public chat (See collage at the start of this document). It only works on a handful of servers at the moment, more can be added in the future. 

## Custom Render Endpoint

Chattycape works best when creative people like yourself come up with their own templates!

Chattycape CLI prompts the user upon every start, if they want to use a custom render endpoint. What this means is that you could easily create your own "texture generator" in whatever language you want, as long as the output is a type `image/png` and satisfies LabyMod's sprite layout:<br>
![Layout](https://storage.googleapis.com/public.victorwesterlund.com/github/VictorWesterlund/chattycape/cape_layout.png)

* Chattycape makes a request to the endpoint every **15 seconds** (limit) with the URLParams `server`, `username` and `tag`.<br>
*Example from default endpoint:* 
```text
https://api.victorwesterlund.com/chattycape?server=us.mineplex.com&username=VicW&tag=immortal
```
| URLParam | Value |
|--|--|
| `server` | IP/Hostname of current server.
| `username` | Case-Sensitive string of Minecraft IGN.
| `tag` | String typecasted to lowercase containing a filtered tag.<br>*Default behavior: Extracts player rank on supported servers.*

* URLParam value will be assigned [`None`](https://docs.python.org/3/library/constants.html#None) for falsy conditions. This includes if a player is unranked (`tag` not found)

## Contribute

If you find any bugs or would like to suggest features, please submit it as an [Issue](https://github.com/VictorWesterlund/chattycape/issues).

Pull requests to this repo are more than welcome!

## License

[GNU General Public License v2.0](https://github.com/VictorWesterlund/chattycape/blob/master/LICENSE)
