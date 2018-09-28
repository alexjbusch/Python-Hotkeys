activation_hotkey = ['ctrl_r','ctrl_l','ctrl_r']  #max length 3 keys
gui_enabled = True
exit_gui_on_script_execution = False
kill_script_on_gui_close = False


from tkinter import *
def run_settings_gui():
    ### still in progress
    root = Tk()
    checkBoxChecked = IntVar()
    checkBoxChecked.set(0)
    checkBox1 = Checkbutton(root, variable=checkBoxChecked, onvalue=1, offvalue=0, text="").pack()

    frame = Frame(root, bg='grey')
    root.mainloop()

#run_settings_gui()
