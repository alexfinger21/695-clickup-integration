import os

# imports needed to make web requests
import requests
import urllib
import json
import re

# imports needed for google docs
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# imports needed for system functions
import os
import time
import sys
import locale
import threading
import queue
import datetime

# for caching the tasks at certain times
import schedule

# imports for UI
from tkinter import *
from tkinter import ttk

# import clickup API
import api.funcs

# import roster loading
from api.load_roster import load_roster

from dotenv import load_dotenv

load_dotenv()

def getStudentEmails(G_member) -> set:
    return set(G_member["StudentEmail"].split(", "))

def sortTasks(t):
    return 0 if t.due_date else 1

def disable_event():
    pass

# tkinter keypress event (the barcode reader functions as a keyboard) - only allow digits for the user id's
def keydown(e):
#    global G_win_mode
    keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for k in keys:
        print(k)
        if (e.char == k):
            key_queue.put(k)
            break
    # set the '*' key to a test user
    if (e.char == '*'):
        key_queue.put('2')
        key_queue.put('8')
        key_queue.put('0')

# init json file
api.funcs.cache_tasks()

# update thurs 6:00 pm and saturday 
schedule.every().day.at("15:00").do(api.funcs.cache_tasks)
schedule.every().saturday.at("09:00").do(api.funcs.cache_tasks)
schedule.every().sunday.at("09:00").do(api.funcs.cache_tasks)

if __name__ == "__main__":
    print("===> Starting Time Clock Application")
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    mypath = os.path.dirname(os.path.realpath(__file__)) + "/"

    timeformat = "%Y-%m-%d %H:%M:%S"
    key_queue = queue.Queue()

    # Variables for screen
    clockx = 1
    clockdx = 6
    clocky = 1
    clockdy = 2
    clockcolor = 'blue'

    task_queue = queue.Queue()

    user_name = ""
    
    print("==> Setting credentials")
    # set our credentials to access google docs
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(mypath + 'client_secret_695.json', scope)
    client = gspread.authorize(creds)
    print("==> Credentials set")

    # DEBUGGING (Checking accessible sheets)
    for sheet in client.openall():
        print("Accessible:", sheet.title)
    

    # open workbook
    print("==> Opening workbook")
    G_workbook = client.open(os.getenv("G_WORKBOOK_NAME"))
    print("==> Workbook opened")
    
    # DEBUGGING (Checking available tabs/worksheets)
    print("Worksheets:", [ws.title for ws in G_workbook.worksheets()])

    # get workbook tabs
    G_sheet_roster = G_workbook.worksheet(os.getenv("G_SHEET_NAME"))
    #G_sheet_timelog = G_workbook.worksheet("TimeLog")

    # roster memory structure
    G_roster = {}
    G_roster = load_roster(mypath, G_sheet_roster) # try loading from local file first, then google

    # main window
    rows, cols = (3, 16)
    arr = rows * [[0] * cols]
    G_main = Tk()
    G_main.configure(cursor="none", background="black")
    G_main.attributes("-fullscreen", True)
    G_main.geometry("800x480") # pi screen is 800x480
    G_main.bind("<KeyPress>", keydown)
    clock = Label(G_main, text="00:00:00", bg="black", anchor='w')
    who = Label(G_main, text="Who's here today", fg="SteelBlue1", bg="black", font='Arial 20 bold', anchor='w')
    #tasks = Label(G_main, text=taskText, fg="lime", bg="black", font='Arial 10')

    image = PhotoImage(file = mypath + "695.png")
    imagelab = Label(G_main, image=image, borderwidth=0)

    G_win = Toplevel(G_main)
    G_win.geometry("") # was (769x97) but i set to empty because it autosizes correctly
    G_win.configure(cursor="none", background="tan4")
    G_win.transient(G_main)
    G_win.overrideredirect(1)

    #NOTE: Variables
    current_user=StringVar()
    todo_tasks=StringVar()
    todo_name=StringVar()
    inprogress_tasks=StringVar()
    inprogress_name=StringVar()
    subteam_tasks=StringVar()
    subteam_name=StringVar()

    #NOTE: Task Display UI
    tasks_header = Label(G_main, textvariable=current_user, bg="black", fg="white", font='Arial 11', anchor='center')
    tasks_header.place(relx=0.5, rely=0.45, anchor='s')
    inprogress_header = Label(G_main, textvariable=inprogress_name, bg="black", fg="#EE5E99", font='Arial 11', anchor='center')
    inprogress_header.place(relx=0.2, rely=0.465)
    inprogress_label = Label(G_main, textvariable=inprogress_tasks, bg="black", fg="#EE5E99", font='Arial 11', anchor='e', justify="left", wraplength=370)
    inprogress_label.place(relx=0.01, rely=0.52)
    todo_header = Label(G_main, textvariable=todo_name, bg="black", fg="#c1c1c1", font='Arial 11', anchor='center')
    todo_header.place(relx=0.72, rely=0.465)
    todo_label = Label(G_main, textvariable=todo_tasks, bg="black", fg="#c1c1c1", font='Arial 11', anchor='e', justify="left", wraplength=360)
    todo_label.place(relx=0.55, rely=0.52)
    subteam_header = Label(G_main, textvariable=subteam_name, bg="black", fg="#c1c1c1", font='Arial 11', anchor='center', justify="left", wraplength=360)
    subteam_header.place(relx=0.42, rely=0.79)
    subteam_label = Label(G_main, textvariable=subteam_tasks, bg="black", fg="#c1c1c1", font='Arial 11', anchor='center', justify="left", wraplength=360)
    subteam_label.place(relx=0.40, rely=0.82)

    #NOTE: Loading bar animation
    # Hand animating gif as tkinter doesn't support animated gifs by default
    frameCnt = 6 # num of frames in gif
    frames = [PhotoImage(file = mypath + "loadingBison.gif",format = 'gif -index %i' %(i)) for i in range(frameCnt)]

    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        loadingImageLab.configure(image=frame)
        G_main.after(100, update, ind)

    loadingImageLab = Label(G_main, bg="black")
    

    #run the update command
    G_main.after(0, update, 0)
    

    for r in range(0, 3):
        for c in range(0,16):
            mtxt = ""
            for member in G_roster:
                if member["grow"] == r + 1 and member["gcol"] == c + 1:
                    mtxt = member["StudentFirst"]
                    print(member["StudentFirst"])
                    #mtxt = member["StudentFirst"][0] + member["StudentLast"][0]
                    if "ClockIn" in member:
                        fgcolor = "yellow"
                    else:
                        fgcolor = "gray20"
            Label(G_win,
            text = mtxt,
            font = ("Arial", 8, "bold"),
            fg = fgcolor,
            bg = "black",
            justify = "center",
            width = 7,
            height = 2).grid(row = r, column = c, sticky = W, padx = 1, pady = 1)

    # main program loop
    user_id = ""
    while True:
        schedule.run_pending() # schedule loop

        # run this loop every 100 msec for timely barcode clock in/out processing
        # keep window at the foreground
        #G_win.grab_set()

        #reset grid positioning
        G_win.geometry(f"+{G_main.winfo_x() + 14}+{G_main.winfo_y() + 60}")
        
        G_main.update()
        

        time.sleep(0.1)

        #NOTE - change later
        #screensave = True
        screensave = False
        for member in G_roster:
            if "ClockIn" in member:
                screensave = False
                break

        curtime = datetime.datetime.now().strftime('%H:%M:%S')
        clock.config(text=curtime)
        if screensave == True:
            G_win.withdraw()
            who.place_forget()
            clock.place_forget()
            #clock.config(fg=clockcolor, font='Arial 20 bold')
            #clock.place(x=clockx, y=clocky)
            imagelab.place(x=clockx, y=clocky)
            colorchange = False

            tx = G_main.winfo_width()
            if clockx + clockdx < 0 or clockx + clockdx > tx - imagelab.winfo_width():
                clockdx *= -1
                colorchange = True
            clockx = clockx + clockdx

            ty = G_main.winfo_height()
            if clocky + clockdy < 0 or clocky + clockdy > ty - imagelab.winfo_height():
                clockdy *= -1
                colorchange = True
            clocky = clocky + clockdy

            if colorchange == True:
                if clockcolor == 'blue':
                    clockcolor = 'red'
                else:
                    clockcolor = 'blue'

        else:
            G_win.deiconify()
            who.place(x=1, y=1)
            imagelab.place_forget()
            clock.config(fg='firebrick1', font='Arial 20 bold')
            clock.place(x=G_main.winfo_width() - clock.winfo_width(), y=1)

        if key_queue.empty():
            user_id = ""
        else:
            while not key_queue.empty():
                print(key_queue.empty())
                user_id = user_id + key_queue.get()

        try:
            while not task_queue.empty():
                item = task_queue.get_nowait()
                if item == "TASKS_LOADED":
                    loadingImageLab.place_forget() # forget where the image is
                elif isinstance(item, tuple):
                    if item[0] == "TO_DO":
                        todo_name.set("To Do")
                        todo_tasks.set(item[1])
                    elif item[0] == "IN_PROGRESS":
                        inprogress_name.set("In Progress")
                        inprogress_tasks.set(item[1])
                    elif item[0] == "SUBTEAM":
                        subteam_name.set(f"General {G_member['Survey2024']} Tasks")
                        subteam_tasks.set(item[1])
        except queue.Empty:
            pass  # Queue is empty, continue with the next iteration

        # user id must be 3 digits, so just loop if nothing to look up yet
        # print("UID: " + user_id)
        if len(user_id) != 3:
            continue

        # confirm valid user
        user_found = False
        for member in G_roster:
            if member["BarcodeID"] == user_id:
                user_found = True
                G_member = member

                grow = member["grow"]
                gcol = member["gcol"]
                break

        if user_found == True:
            for child in G_win.winfo_children():

                if type(child) != Label:
                    continue

                r = child.grid_info()['row'] + 1
                c = child.grid_info()['column'] + 1

                if r == grow and c == gcol:
                    if "ClockIn" not in G_member:
                        loadingImageLab.place(relx=0.5, rely=0.5, anchor=CENTER)

                        #remove current user
                        current_user.set("")

                        #reset task display
                        todo_tasks.set("")
                        inprogress_tasks.set("")

                        #reset headers
                        todo_name.set("")
                        inprogress_name.set("")

                        #set user
                        user_name = G_member['StudentFirst']
                        current_user.set(f"Tasks for {G_member['StudentFirst']}")

                        # display all tasks for all emails for student
                        def task_thread():
                            user = user_name
                            tasks = api.funcs.display_tasks(getStudentEmails(G_member), {"in progress", "to do"}, G_member["Survey2024"]) or ""
                            st_tasks = sorted(tasks[0], key=sortTasks)[:3]
                            usr_tasks = sorted(tasks[1], key=sortTasks)[:6]

                            if user == user_name:
                                while not task_queue.empty():
                                    task_queue.get_nowait()
                            else:
                                return

                            todo_tasks_str = "\n".join([str(task) for task in usr_tasks if task.status.get("status")=="to do"])
                            inprogress_tasks_str = "\n".join([str(task) for task in usr_tasks if task.status.get("status")=="in progress"])
                            st_tasks_str = "\n".join([str(task) for task in st_tasks])

                            task_queue.put_nowait(("TO_DO", todo_tasks_str if todo_tasks_str else "To Do: None"))
                            task_queue.put_nowait(("IN_PROGRESS", inprogress_tasks_str if inprogress_tasks_str else "In Progress: None"))
                            task_queue.put_nowait(("SUBTEAM", st_tasks_str if st_tasks_str else "None"))
                            task_queue.put_nowait("TASKS_LOADED")

                            


                        new_thread = threading.Thread(target=task_thread)
                        new_thread.start()

                        G_member["ClockIn"] = datetime.datetime.now().strftime(timeformat)
                        child['fg'] = "yellow"
                        print(G_member["ClockIn"] + " CLOCK IN:  " + G_member["StudentFirst"])
                    else:
                        #remove current user
                        current_user.set("")

                        #reset task display
                        todo_tasks.set("")
                        inprogress_tasks.set("")
                        subteam_tasks.set("")

                        #reset headers
                        todo_name.set("")
                        inprogress_name.set("")
                        subteam_name.set("")

                        # clock out
                        G_member["ClockOut"] = datetime.datetime.now().strftime(timeformat)

                        # compute change in time and write to log file
                        delta = datetime.datetime.strptime(G_member["ClockOut"], timeformat) - datetime.datetime.strptime(G_member["ClockIn"], timeformat)
                        l = G_member["BarcodeID"] + "\t" + G_member["StudentFirst"] + "\t" + G_member["ClockIn"] + "\t" + G_member["ClockOut"] + "\t" + str(delta.total_seconds()) + "\r\n"
                        f = open(mypath + "logs/{d.year}{d.month:02}{d.day:02}.log".format(d=datetime.datetime.now()), "a")
                        f.write(l)
                        f.close()
                        child['fg'] = "gray20"
                        print(G_member["ClockOut"] + " CLOCK OUT: " + G_member["StudentFirst"])
                        del G_member["ClockIn"]
                        del G_member["ClockOut"]

                    f = open(mypath + "roster.json", "w")
                    f.write(json.dumps(G_roster, indent=4))
                    f.close()

 
