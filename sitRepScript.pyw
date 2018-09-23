from bs4 import *
from urllib.request import urlopen
from tkinter import *
import webbrowser
import pickle

status_dict = {"xkcd":2047,"smbc":2}


def get_current_xkcd():
    main_page = urlopen("https://xkcd.com")
    soup = BeautifulSoup(main_page,'html.parser')
    div = soup.find('div',{"id":"middleContainer"})
    comic = str(div).split("Permanent link to this comic: https://xkcd.com/",1)[1].split("/")[0]
    return int(comic)

def xkcd_status():
    current_xkcd = get_current_xkcd()
    if current_xkcd != status_dict["xkcd"]:
        
        unread_count = current_xkcd-status_dict["xkcd"]

        new_comic = status_dict["xkcd"]+1
        page = urlopen("https://xkcd.com//%s"% str(new_comic))
        #page.getcode()   # line for testing
        status_dict["xkcd"] = new_comic
        
        if unread_count > 1:
            plural_s = "s"
        else:
            plural_s = ""
        ###     found new comic, return tuple of url and string for the link
        return (page.url,str(unread_count)+" new unread xkcd comic%s!"%plural_s)
    else:
        ###     no new comics, return None
        return


def open_chrome(url):
    webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(url)

def set_current_all():
    status_dict["xkcd"] = get_current_xkcd()
    ###  TODO ADD MORE SITES TO CHECK AND SET THEM CURRENT HERE

def set_almost_current_all():
    status_dict["xkcd"] = get_current_xkcd()-1
    
def load_data():
    try:
        file = open("sitRep_data.txt",'rb')
        global status_dict
        try:
            status_dict = pickle.load(file)
        except (EOFError,pickle.UnpicklingError):
            set_current_all()
    except FileNotFoundError:
        set_almost_current_all()
        
def make_report():
    new_xkcd = xkcd_status()
    if new_xkcd != None:
        link = Label(root, text=new_xkcd[1], fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda _: open_chrome(new_xkcd[0]))
    else:
        link = Label(root, text="All Current")
        link.pack()
    ### TODO: ADD ADDITIONAL THINGS TO CHECK FOR BESIDES XKCD
    
def save():
    outfile = open("sitRep_data.txt",'wb')
    pickle.dump(status_dict,outfile)
    outfile.close()
    root.destroy()

def main():
    frame = Frame(root, bg='grey')
    root.title("Sit Rep")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.protocol("WM_DELETE_WINDOW", save)

    load_data()
    make_report()

    root.mainloop()


root = Tk()
main()



