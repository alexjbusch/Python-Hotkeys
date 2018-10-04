from pynput.keyboard import Key,Listener
import logging
import re
from tkinter import *
from tkinter import messagebox
import os, subprocess
from functools import partial
from threading import Timer
import os
import json

import settings

# ordinary globals
root = None
listening = False
editing_hotkey = False
object_being_edited = None
gui_enabled = True
press_record = [""] * 11

###  EXTERNAL SCRIPT VARIABLES START HERE
script_data = {"start_repeating":False,"test_var":False,"kill_switch":False}
with open('scripts//script_data.txt', 'w') as outfile:
    json.dump(script_data, outfile)
###  END EXTERNAL SCRIPT VARS


class Hotkey:
    def __init__(self,script_name,hotkey,row):
        self.script_name = script_name
        self.hotkey = hotkey
        self.row = row
        self.text_before_edit = self.script_name
        self.hotkey_before_edit = self.hotkey
        self.add_new_hotkey_button = None
      
    def render(self):
        self.script_name_text = Label(text=self.script_name,relief=RIDGE,padx=110,pady=50,width=15)
        self.hotkey_text = Label(text=" ".join(self.hotkey), relief=RIDGE,width=45)
        self.execute_button = Button(root, text="Execute Script", padx=10,command=partial(run, self.script_name))
        self.edit_hotkey_button = Button(root,command=self.edit_hotkey,text="Edit Hotkey", padx=10)
        self.edit_script_button = Button(root,command=self.edit_script_name,text="Edit Script", padx=10)

        self.edit_script_button.grid(row=self.row,column=0)
        self.script_name_text.grid(row=self.row,column=1)
        self.hotkey_text.grid(row=self.row,column=2)
        self.execute_button.grid(row=self.row,column=3)
        self.edit_hotkey_button.place(in_=self.hotkey_text,relx=.37,rely=-2)
      
    def edit_hotkey(self):
        global listening
        listening = False
        global editing_hotkey
        editing_hotkey = True
        self.hotkey_before_edit = self.hotkey
        self.hotkey = ["","",""]
        self.text_before_edit = self.hotkey_text.cget("text")
        self.hotkey_text.config(bg='light blue',text="Press any key")
        self.edit_hotkey_button.config(text="Save New Hotkey",command=self.save_hotkey)
        global object_being_edited      
        if object_being_edited != None and object_being_edited != self:
            object_being_edited.cancel_edit()
        object_being_edited = self

    def edit_script_name(self):
        global editing_hotkey
        editing_hotkey = False
        global listening
        listening = False
        self.text_before_edit = self.script_name
        self.edit_script_button.config(text="Save New Script",command=self.save_script_name)
        
        self.script_name_text = Text(root, height=2, width=30)
        self.script_name_text.insert(END,self.script_name)        
        self.script_name_text.grid(row=self.row,column=1)
        global object_being_edited
        if object_being_edited != None and object_being_edited != self:
            object_being_edited.cancel_edit()
        object_being_edited = self

    def save_hotkey(self):        
        global listening
        global press_record
        if self.hotkey == ["","",""]:
            self.hotkey = self.hotkey_before_edit            
        self.hotkey_text.config(text=" ".join(self.hotkey),bg="SystemButtonFace")
        self.edit_hotkey_button.config(command=self.edit_hotkey,text="Edit Hotkey")
        press_record = [""] * 11
        listening = True
        object_being_edited = None

    def save_script_name(self):
        global listening
        global press_record
        self.script_name = self.script_name_text.get("1.0",END)[:-1]  #for some reason tkinter's .get() function returns a string with a space at the end
        self.script_name = self.script_name.replace('\n',' ').strip()
        self.script_name_text = Label(text=self.script_name,relief=RIDGE,padx=110,pady=50,width=15)
        self.edit_script_button.config(command=self.edit_script_name,text="Edit Script")
        self.script_name_text.grid(row=self.row,column=1)
        self.execute_button.config(command=partial(run, self.script_name))
        press_record = [""] * 11
        listening = True
        object_being_edited = None
        
    def cancel_edit(self):
        ### this function resets the gui when you edit something else without saving
        self.hotkey_text.config(bg="SystemButtonFace",text=" ".join(self.hotkey_before_edit))
        self.edit_hotkey_button.config(command=self.edit_hotkey,text="Edit Hotkey")
        self.edit_script_button.config(command=self.edit_script_name,text="Edit Script")
        self.script_name_text = Label(text=self.script_name,relief=RIDGE,padx=110,pady=50,width=15)
        self.script_name_text.grid(row=self.row,column=1)
        
###  this is where default hotkeys are stored.  this line has to be called down here so that it has access to the hotkey class
###  CONSIDER: moving this to json
hotkey_codex = [Hotkey("test.py",["+","+","5"],0),Hotkey("repeaterScript.pyw",["+","+","6"],1),Hotkey("sitRepScript.pyw",["+","+","8"],2)]


def Main():
    # this is where tkinter and pynput are threaded
    t = Timer(0, create_popup)
    t.start()
    with Listener(on_release=on_release) as listener:
        listener.join()

def on_gui_close():
    if settings.kill_script_on_gui_close:
        os._exit(0)  # TODO: CONSIDER CHANGING TO SYS.EXIT SOMEHOW
    global listening
    listening = False
    root.destroy()
    create_popup()

    
def create_popup():
    # tkinter is initialized here
    global root
    root = Tk()
    frame = Frame(root, bg='grey')
    for i in hotkey_codex:
        i.render()
    hotkey_codex[-1].add_new_hotkey_button = Button(root,command=add_new_hotkey,text="Add New Hotkey", padx=10)
    hotkey_codex[-1].add_new_hotkey_button.place(in_=hotkey_codex[-1].hotkey_text,relx=.37,rely=4)

    root.title("Central Command Menu")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", on_gui_close)
    root.mainloop()

def add_new_hotkey():
    # creates a new instance of the hotkey class and adds renders it in the gui
    new_hotkey = Hotkey("",["","",""],hotkey_codex[-1].row+1)

    hotkey_codex[-1].add_new_hotkey_button.destroy()
    hotkey_codex.append(new_hotkey)
    new_hotkey.render()  
    new_hotkey.add_new_hotkey_button = Button(root,command=add_new_hotkey,text="Add New Hotkey", padx=10)
    new_hotkey.add_new_hotkey_button.place(in_=new_hotkey.hotkey_text,relx=.37,rely=4)


def run(file_name):
    if file_name != "":
        try:
            os.startfile(os.path.dirname(os.path.realpath(__file__))+"\\scripts\\"+file_name)
            if settings.exit_gui_on_script_execution:
                root.destroy()
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "No file found by the name " + file_name)
    else:
        messagebox.showinfo("No File Specified", "Please Enter the Name of a File Before Trying to Execute")

def emergency_shutdown():
    os.system("taskkill /im pythonw.exe")

def on_release(key):
    handle_keys(key)

def on_press(key):
    handle_keys(key)
    
def handle_keys(key):
    global listening    
    key = str(key)
    key = key.replace("'","")
    key = key.replace("Key.","")
    global press_record
    press_record.insert(0,key)
    press_record = press_record[0:10]
    
    print(key)

    if not listening:
        if editing_hotkey and object_being_edited != None:
            hotkey_full = True
            for i in range(len(object_being_edited.hotkey)):              
                if object_being_edited.hotkey[i] == "":
                    object_being_edited.hotkey[i] = key
                    object_being_edited.hotkey_text.config(text=" ".join(object_being_edited.hotkey))
                    hotkey_full = False
                    break
            if hotkey_full:
                object_being_edited.hotkey = [key,"",""]
                object_being_edited.hotkey_text.config(text=" ".join(object_being_edited.hotkey))

        else:
            if press_record[0:3] == settings.activation_hotkey:
                listening = True
                press_record = [""] * 11
                ### gui is turned on here
                if settings.gui_enabled:
                    root.deiconify()

    elif listening:
        if key == "esc":
            ### TODO: find out how to cancel running scripts via hotkeys
            ### POSSIBLE SOLUTION: use json variables to order self termination
            #emergency_shutdown()
            root.destroy()
            listening = False
        elif key == "space":
            script_data["start_repeating"] = True
            with open('scripts//script_data.txt', 'w') as outfile:
                json.dump(script_data, outfile)
        else:
            for i in hotkey_codex:
                # TODO: MAKE ACTIVATION HOTKEY VARIABLE LENGTH
                if "".join(press_record[0:3]) == "".join(reversed(i.hotkey)):
                    press_record = [""] * 11
                    run(i.script_name)

Main()

