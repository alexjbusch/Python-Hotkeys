from bs4 import *
from urllib.request import urlopen
from urllib.error import *
import re
from tkinter import *
import webbrowser
import pickle
import time

# TODO : GET MULTITHREADING WORKING
# TODO : MAKE NETFLIX SHOWS ADDABLE VIA SETTINGS


start_time = None

status_dict = {"xkcd":2047,"smbc":"September 9, 2018","Better_Call_Saul":(3,6)}
netflix_shows = [("Better_Call_Saul",80021955)]

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

def get_new_netflix_episodes(show):
    show_name = show[0]
    show_number = show[1]
    page = urlopen("https://www.netflix.com/title/"+str(show_number))
    soup = BeautifulSoup(page,'html.parser')
    scripts = soup.find_all("script")
    brackets =  re.findall(r'{(.*?)}',str(scripts[11]))
    episodes = []
    for i in brackets:
        if "\"episodeNum\":" in i:
            season = re.search(r'\"num\":(.*?),',i)[1]
            episode = re.findall(r'\"episodeNum\":(.*?),',i)[0]
            link = re.findall(r'\"episodeId\":(.*?),',i)[0]
            episodes.append((season,episode,link))

    next_episode = None
    current_episode_found = False
    new_episode_count = None
    for i in episodes:
        if current_episode_found:
            # this is the next episode since the current one
            next_episode = i
            # this is the number of new episodes out
            new_episode_count = episodes.index(episodes[-1]) - episodes.index(i) + 1
            break
        # check if this is the current episode
        if i[0] == str(status_dict[show_name][0]) and i[1] == str(status_dict[show_name][1]):
            current_episode_found = True
    # new episode(s) found, return link and string for link text
    if next_episode != None:
        plural_var = ""
        if new_episode_count > 1:
            plural_var = "s"
        elif new_episode_count == 1:
            plural_var = ""
        # this sets the status dict current (to the last episode found)
        status_dict[show_name] = (episodes[-1][0],episodes[-1][1])
        # TODO: TURN THE UNDERSCORES IN THE SHOW NAME INTO SPACES
        return ("https://www.netflix.com/watch/" + next_episode[2],str(new_episode_count)+" new "+show_name+" episode"+plural_var)
    # no new netflix episodes for this show, return None
    else:
        return

def get_newest_netflix_episode(show,get_second_newest=False):
    page = urlopen("https://www.netflix.com/title/"+str(show[1]))
    soup = BeautifulSoup(page,'html.parser')
    scripts = soup.find_all("script")
    brackets =  re.findall(r'{(.*?)}',str(scripts[11]))
    # return a tuple of season and episode number
    if get_second_newest:
        # this returns the second to last episode
        return (re.findall(r'\"num\":(.*?),',str(brackets))[-2],re.findall(r'\"episodeNum\":(.*?),',str(brackets))[-2])
    # this returns the last episode
    return (re.findall(r'\"num\":(.*?),',str(brackets))[-1],re.findall(r'\"episodeNum\":(.*?),',str(brackets))[-1])
    
def open_chrome(url):
    webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(url)

def set_current_all():
    # xkcd
    status_dict["xkcd"] = get_current_xkcd()
    # smbc
    soup = BeautifulSoup(urlopen("https://www.smbc-comics.com/comic/archive"),'html.parser')
    archive = soup.find_all('option')
    status_dict["smbc"] = archive[-1].text.split(" -")[0]
    # netflix
    for i in netflix_shows:
        status_dict[i[0]] = get_newest_netflix_episode(i)

def set_almost_current_all():
    # xkcd
    status_dict["xkcd"] = get_current_xkcd()-1
    # smbc
    soup = BeautifulSoup(urlopen("https://www.smbc-comics.com/comic/archive"),'html.parser')
    archive = soup.find_all('option')
    status_dict["smbc"] = archive[-2].text.split(" -")[0]
    
    # netflix
    for i in netflix_shows:
        status_dict[i[0]] = get_newest_netflix_episode(i,get_second_newest=True)
    
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
    
    new_xkcd = xkcd_status()
    new_smbc = smbc_status()
    if new_xkcd != None:
        make_link(new_xkcd)
    if new_smbc != None:
        make_link(new_smbc)
    
    for i in netflix_shows:
        new_episodes = get_new_netflix_episodes(i)
        if new_episodes != None:
            make_link(new_episodes)
            
        
    if all_current:
        link = Label(root, text="All Current")
        link.pack()
    print(time.time()-start_time)
    
    
def save():
    outfile = open("sitRep_data.txt",'wb')
    pickle.dump(status_dict,outfile)
    outfile.close()
    root.destroy()

def main():
    global start_time
    start_time = time.time()
    frame = Frame(root, bg='grey')
    root.title("Sit Rep")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.protocol("WM_DELETE_WINDOW", save)

    load_data()
    make_report()

    root.mainloop()

root = Tk()
main()



