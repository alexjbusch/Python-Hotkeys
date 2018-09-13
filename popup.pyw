from pynput.keyboard import Key,Listener
import logging
import re
from tkinter import *
import os, subprocess
from functools import partial
from listener import script_codex,run

tk = None
def create(script_codex):
   print(script_codex)
   global tk
   tk = Tk()
   Frame(tk, bg='grey')

   
   index = 0
   while index < len(script_codex):
      Label(text=script_codex[index][0],relief=RIDGE,pady=50,width=15).grid(row=index,column=0)
      Label(text=script_codex[index][1], relief=RIDGE,width=45).grid(row=index,column=1)
      Button(tk, text="Execute Script", padx=10,command=partial(run, script_codex[index][0])).grid(row=index,column=2)
      index += 1

   tk.title("Central Command Menu")
   tk.mainloop()

def destroy():
   global tk
   tk.quit()


#if __name__ == "__main__":
   #test_codex = [("",""),("",""),("","")]
create(script_codex)
