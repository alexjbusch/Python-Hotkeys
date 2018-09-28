# Python-Hotkeys
A collection of convenient python scripts that can be called via hotkeys.

### Instructions For Use
To start the listener, simply run listener.pyw, which initially listens only for the activation hotkey. The activation hotkey defaults to "CTRL_RIGHT  CTRL_LEFT  CTRL_RIGHT", and when pressed will bring up the gui and begin listening for hotkeys tied to scripts.  From the gui you can run default scripts, add your own, modify existing hotkeys, and most importantly trigger scripts via keypresses. Be advised that listener.pyw doesn't terminate after the gui is closed by default, so it will have to be closed manually from task manager or the terminal.  

### Settings
The activation hotkey, as well as preferences for whether the gui pops up or not, and whether the gui closes upon script execution are all editable from the file settings.py.  If you wish to edit the default hotkey manually in settings.py, please use pynput key codes, which can be found here: https://pythonhosted.org/pynput/keyboard.html.  Please note that the beginning parts of the key codes are unnecessary, so "pynput.keyboard.Key.num_lock" should be rendered simply as the string "num_lock" in the activation hotkey list.  Future versions will include a gui for changing the settings. 

Python-Hotkeys lets you create your own hotkeys and bind them however you want, but the following scripts have been added as defaults:
## test.py
This script merely prints out "Your hotkey is working" in an infinite loop.  Useful for testing purposes when adding your own hotkeys.

## sitRepScript
sitRepScript is meant to act as a centralized way to quickly check if media you're following has new content without actually having to navigate to any websites.  It currently only checks for how many xkcd comics have come out since you last ran the script, but future updates will include checking for new gmail or facebook messages, other webcomics such as smbc, new episodes of shows on netflix, and new youtube videos from specific channels.  If all media are up to date, the popup will simply display the text "All Current".  Otherwise it will print out a set of links announcing how many new content objects have come out.  When the links are clicked, they open up google chrome and navigate automatically to the new media in question.  Future updates may include support for Firefox and Safari but not Microsoft Edge (for moral reasons).  

This software uses python scripts, and thus requires a python interpreter.
If you’re interested in using this software on a windows computer without python installed, you should check out the dependency free version of this software in the All-EXE branch:  
https://github.com/alexjbusch/Python-Hotkeys/tree/All-EXE

