from bs4 import *
from urllib.request import urlopen
from urllib.error import *
import re
from tkinter import *
import webbrowser
import pickle
import time
status_dict = {"xkcd":2047,"smbc":"September 9, 2018",}

all_current = True

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

def smbc_status():
    start_time = time.time()
    
    soup = BeautifulSoup(urlopen("https://www.smbc-comics.com/comic/archive"),'html.parser')
    archive = soup.find_all('option')
    index = 0
    for i in reversed(archive):
        ###  found new comic, return tuple of url and string for the link
        if status_dict["smbc"] in i.text:
            if i != archive[-1]:
                status_dict["smbc"] = archive[-1].text.split(" -")[0]
                if index > 1:
                    plural_s = "s"
                else:
                    plural_s = ""
                return ("https://www.smbc-comics.com/"+str(i.next_sibling.attrs["value"]),(str(index)+" new unread smbc comic%s!"%plural_s))
        index += 1
    ### no new comics found, return None
    return
    #print(time.time() - start_time)

def get_new_netflix_episodes(show):
    
    page = urlopen("https://www.netflix.com/title/"+str(show))
    soup = BeautifulSoup(page,'html.parser')
    scripts = soup.find_all("script")
    episode_numbers = re.findall(r'\"episodeNum\":(.*?),',str(scripts[11]))
    episode_links =re.findall(r'\"episodeId\":(.*?),',str(scripts[11]))

    ### TODO: WRITE LOGIC HERE THAT CHECKS IF NEW EPISODES HAVE COME OUT SINCE THE LAST TIME YOU RAN THE SCRIPT
    return ("https://www.netflix.com/watch/" + episode_links[-1],"the newest episode is ep. " + episode_numbers[-1])
    
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

def make_link(link_string):
    global all_current
    all_current = False
    link = Label(root, text=link_string[1], fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda _: open_chrome(link_string[0]))
def make_report():
    print(get_new_netflix_episodes(80117365))
    new_xkcd = xkcd_status()
    new_smbc = smbc_status()
    print(new_smbc)
    if new_xkcd != None:
        make_link(new_xkcd)
    if new_smbc != None:

        make_link(new_smbc)
    if all_current:
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



