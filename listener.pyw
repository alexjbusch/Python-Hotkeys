from pynput.keyboard import Key,Listener
import logging
import re
from tkinter import *
import os, subprocess
import popup

#label = Label(master, text="This is our first GUI!")
#greet_button = Button(master, text="Greet", command=self.greet)
#close_button = Button(master, text="Close", command=master.quit)

script_codex = [("hello.exe","26"),("test.py","45")]
def Main():
   with Listener(on_press=on_press) as listener:
    listener.join()

def run(file_name):
    os.startfile(os.path.dirname(os.path.realpath(__file__))+"\\"+file_name)
    
def generate_popup():
    tk = Tk()
    Frame(tk, bg='grey').pack()
    tk.attributes("-fullscreen", True)
    tk.pack_propagate(1)
    Label(tk, text="This is our first GUI!")
    tk.title("Central Command Menu")
    tk.mainloop()



    
scripts = ["helloWorld","repeaterScript","statusUpdate"]

message_format = ""
for i in scripts:
    message_format += (i+"\n\n\n")



listening = False
press_record = []
press_record = [""] * 11

def on_press(key):
    key = str(key)
    if "'" in key:
      key = key.replace("'","")  
    global press_record

    press_record.insert(0,key)
    press_record = press_record[0:10]
    #print(press_record)
    print(key)
    
    global listening
    if press_record[0]+press_record[1]+press_record[2] == 'Key.ctrl_rKey.ctrl_lKey.ctrl_r':
        if not listening:
            
            popup.create(script_codex)
            #run("popup.exe")
            listening = True
      
    if listening:
        if key == "Key.esc":
            print(press_record)

if __name__ == "__main__":
   Main()

