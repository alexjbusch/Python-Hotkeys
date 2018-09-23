# Python-Hotkeys
A collection of convenient python scripts that can be called via hotkeys.

Python-Hotkeys lets you create your own hotkeys and bind them however you want, but the following scripts have been added as defaults:

## sitRepScript
sitRepScript is meant to act as a centralized way to quickly check if media you're following has new content without actually having to navigate to any websites.  It currently only checks for how many xkcd comics have come out since you last ran the script, but future updates will include checking for new gmail or facebook messages, other webcomics such as smbc, new episodes of shows on netflix, and new youtube videos from specific channels.  If all media are up to date, the popup will simply display the text "All Current".  Otherwise it will print out a set of links announcing how many new content objects have come out.  When the links are clicked, they open up google chrome and navigate automatically to the new media in question.  Future updates may include support for Firefox and Safari but not Microsoft Edge (for moral reasons).  

This software uses python scripts, and thus requires a python interpreter.
If you’re interested in using this software on a windows computer without python installed, you should check out the dependency free version of this software in the All-EXE branch:  
https://github.com/alexjbusch/Python-Hotkeys/tree/All-EXE

