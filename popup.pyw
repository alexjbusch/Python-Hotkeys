from pynput.keyboard import Key,Listener
import logging
import re
from tkinter import *
import os, subprocess
tk = None
def create():
   global tk
   tk = Tk()
   Frame(tk, bg='grey').pack()
   Button(tk,text="Close",command=tk.quit).pack()
   tk.attributes("-fullscreen", True)
   tk.pack_propagate(1)
   Label(tk, text="This is our first GUI!").pack()
   tk.title("Central Command Menu")
   tk.mainloop()

def destroy():
   global tk
   tk.quit()

create()
