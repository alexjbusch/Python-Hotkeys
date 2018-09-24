import time
import pyHook
import pythoncom
import pyautogui
import sys
import os
from multiprocessing import Process
from threading import Timer
from tkinter import *
finished = False
#import listener
test_bool = False
import_only = True

input_log = []
cycles = 2
time_after_click = 1
time_before_click = .1
root = None
                        
def OnMouseEvent(event):   
    global finished
    if finished == False:
        if (event.MessageName in {"mouse left down","mouse right down","mouse middle down"}):
            input_log.append((event.MessageName,event.Position))

    return True
def OnKeyboardEvent(event):
    global finished
    if finished == False:
        input_log.append((event.Key,None))
    return True

def start_repeating():
    hm.UnhookMouse()
    finished = True
    index = 0
    while index < cycles:
        Mimic_Input()
        index += 1
        time.sleep(time_after_click)
    sys.exit(0)
def Mimic_Input():
    for i in input_log:
        
        if i[0] == "mouse left down":
            pyautogui.moveTo(i[1])
            time.sleep(time_before_click)
            pyautogui.click(button='left')

def start_listening():
    hm = pyHook.HookManager()
    hm.SubscribeMouseAll(OnMouseEvent)
    hm.HookMouse()
    hm.KeyDown = OnKeyboardEvent
    pythoncom.PumpMessages()

def listen_for_instruction():
    while True:
        #if listener.start_repeating:
        if test_bool:
            print("yes")
    
def main():
    global root
    root = Tk()
    frame = Frame(root, bg='grey')
    root.title("repeaterScript")
    Button(root,command=start_listening,text="Start Listening", padx=10).pack()
    t = Timer(0, listen_for_instruction)
    t.start()

#root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#p=Process(target=listen_for_instruction())
if not import_only:
    main()
    print("it ran")
#root.mainloop()




