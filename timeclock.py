# dummy G_roster

G_roster = [
    {"grow": 1, "gcol": 1, "StudentFirst": "John", "StudentLast": "Doe"},
    {"grow": 2, "gcol": 2, "StudentFirst": "Jane", "StudentLast": "Smith", "ClockIn": True},
    {"grow": 3, "gcol": 3, "StudentFirst": "Alice", "StudentLast": "Johnson"},
    {"grow": 1, "gcol": 4, "StudentFirst": "Bob", "StudentLast": "Brown", "ClockIn": True}
]



from tkinter import *
from tkinter import ttk
import datetime
import json
import time
import requests
from queue import Queue

key_queue = Queue()



def keydown(e):
#    global G_win_mode
    keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for k in keys:
        if (e.char == k):
            key_queue.put(k)
            break
    # set the '*' key to a test user
    if (e.char == '*'):
        key_queue.put('2')
        key_queue.put('8')
        key_queue.put('0')


rows, cols = (3, 16)
arr = rows * [[0] * cols]

taskText = "Tasks:\n- Learn ClickUp API\n- Use Clickup API to get actual tasks for people"

G_main = Tk()
G_main.configure(cursor="none", background="black")
G_main.attributes("-fullscreen", True)
G_main.bind("<KeyPress>", keydown)
clock = Label(G_main, text="00:00:00", bg="black", anchor='w')
who = Label(G_main, text="Who's here today", fg="SteelBlue1", bg="black", font='Arial 20 bold', anchor='w')
tasks = Label(G_main, text=taskText, fg="lime", bg="black", font='Arial 10')

#image = PhotoImage(file = mypath + "695.png")
#imagelab = Label(G_main, image=image, borderwidth=0)

G_win = Toplevel(G_main)
#720x98 
G_win.geometry("799x109") # pi screen is 800x480
# for no cursor is:
# G_win.configure(cursor="none", background="tan4")
G_win.configure(background="tan4")
G_win.transient(G_main)
G_win.overrideredirect(1)

for r in range(0, 3):
    for c in range(0,16):
        mtxt = ""
        for member in G_roster:
            if member["grow"] == r + 1 and member["gcol"] == c + 1:
                mtxt = member["StudentFirst"]
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


user_id = ""

while True:
    #run this loop every 100 msec for timely barcode clock in/out processing
    #keep window at the foreground
    G_win.geometry("+40+60")

    G_main.update()

    time.sleep(0.1)

    screensave = True
    for member in G_roster:
        if "ClockIn" in member:
            screensave = False
            break

    curtime = datetime.datetime.now().strftime('%H:%M:%S')
    clock.config(text=curtime)
    
    if screensave:
        G_win.withdraw()
        who.place_forget()
        clock.place_forget()
        tasks.place_forget()
        # uncomment and set position for imagelab if needed
        # imagelab.place(x=clockx, y=clocky)
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

        if colorchange:
            if clockcolor == 'blue':
                clockcolor = 'red'
            else:
                clockcolor = 'blue'
        
    else:
        G_win.deiconify()
        who.place(x=1, y=1)
        # imagelab.place_forget()  # uncomment if using imagelab
        clock.config(fg='firebrick1', font='Arial 20 bold')
        clock.place(x=G_main.winfo_width() - clock.winfo_width(), y=1)
        tasks.place(x=40, y=200)

    if key_queue.empty():
        user_id = ""
    else:
        while not key_queue.empty():
            user_id += key_queue.get()

    # user id must be 3 digits, so just loop if nothing to look up yet
    if len(user_id) != 3:
        continue

    # confirm valid user
    user_found = False
    for member in G_roster:
        if member.get("BarcodeID") == user_id:
            user_found = True
            G_member = member
            grow = member["grow"]
            gcol = member["gcol"]
            break

    if user_found:
        for child in G_win.winfo_children():
            if not isinstance(child, Label):
                continue

            r = child.grid_info()['row'] + 1
            c = child.grid_info()['column'] + 1

            if r == grow and c == gcol:
                if "ClockIn" not in G_member:
                    G_member["ClockIn"] = datetime.datetime.now().strftime('%H:%M:%S')
                    child['fg'] = "yellow"
                    print(G_member["ClockIn"] + " CLOCK IN: " + G_member["StudentFirst"])
                    
                    # taskText = list of tasks from user
                else:
                    G_member["ClockOut"] = datetime.datetime.now().strftime('%H:%M:%S')
                    delta = datetime.datetime.strptime(G_member["ClockOut"], '%H:%M:%S') - datetime.datetime.strptime(G_member["ClockIn"], '%H:%M:%S')
                    l = f"{G_member['BarcodeID']}\t{G_member['StudentFirst']}\t{G_member['ClockIn']}\t{G_member['ClockOut']}\t{delta.total_seconds()}\r\n"
                    with open(mypath + f"logs/{datetime.datetime.now():%Y%m%d}.log", "a") as f:
                        f.write(l)
                    child['fg'] = "gray20"
                    print(G_member["ClockOut"] + " CLOCK OUT: " + G_member["StudentFirst"])
                    del G_member["ClockIn"]
                    del G_member["ClockOut"]
                
                with open(mypath + "roster.json", "w") as f:
                    f.write(json.dumps(G_roster, indent=4))

G_main.mainloop()

