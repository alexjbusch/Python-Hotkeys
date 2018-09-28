import time
import pyHook
import pythoncom
import pyautogui
import sys
import os
from multiprocessing import Process
from threading import Timer
from tkinter import *
import json

finished = False
listening = False



input_log = []
cycles = 2
time_after_click = 1
time_before_click = .1
root = None
hm = None

#make into class
repetitions = None
                    
def OnMouseEvent(event):   
    global finished
    if finished == False:
        if (event.MessageName in {"mouse left down","mouse right down","mouse middle down"}):
            input_log.append((event.MessageName,event.Position))
    return True

def start_repeating():
    #global cycles
    #cycles = int(repetitions.get(1.0,"end-1c"))
    #print (cycles)
        
    hm.UnhookMouse()
    finished = True
    index = 0
    while index < cycles:
        Mimic_Input()
        index += 1
        time.sleep(time_after_click)
    os._exit(0)
def Mimic_Input():
    for i in input_log:
        
        if i[0] == "mouse left down":
            pyautogui.moveTo(i[1])
            time.sleep(time_before_click)
            pyautogui.click(button='left')

def start_listening():
    global listening
    listening = True
    global hm
    hm = pyHook.HookManager()
    hm.SubscribeMouseAll(OnMouseEvent)
    hm.HookMouse()
    #hm.KeyDown = OnKeyboardEvent
    pythoncom.PumpMessages()

def listen_for_instruction():
    ### TODO: FIGURE OUT HOW THIS SCRIPT CAN BE RUN WITHOUT HOTKEY WRAPPER BY
    ###       ACCOUNTING FOR PATH DIFFERENCE. CURRENTLY ONLY WORKS WITH WRAPPER
    path = 'scripts//script_data.txt'
    cached_stamp = os.stat(os.path.abspath(path)).st_mtime
    while True:
        stamp = os.stat(os.path.abspath(path)).st_mtime
        if stamp != cached_stamp:
            cached_stamp = stamp
            with open(path) as json_file:  
                script_data = json.load(json_file)
                if script_data["start_repeating"] == True:
                    script_data["start_repeating"] = False
                    ### WARNING: this rewrites all script data,
                    ### so it will do strange things if running multiple scripts 
                    ### TODO: find a way to modify only one variable of the json file
                    with open('scripts//script_data.txt', 'w') as outfile:
                        json.dump(script_data, outfile)
                    if listening:
                        print("here")
                        start_repeating()
                        return
def onTextEntry(text):
    print(text)
    
def main():
    global root
    root = Tk()
    frame = Frame(root, bg='grey')
    root.title("repeaterScript")
    #TODO: MAKE THIS INTO A CLASS
    '''
    global repetitions
    repetitions = Text(root,height=2, width=3)
    repetitions.insert(END, "1")
    repetitions.grid(row=0,column=1)
    
    time_before_click_box = Text(root,height=2, width=3).grid(row=1,column=1)
    time_after_click_box = Text(root,height=2, width=3).grid(row=2,column=1)
    '''
    Button(root,command=start_listening,text="Start Listening", padx=10).grid(row=3,column=2)
   #print(root.winfo_children())

    root.geometry("{0}x{1}+0+0".format(400, 500))
    t = Timer(0, listen_for_instruction)
    t.start()    
    root.mainloop()
    

main()
