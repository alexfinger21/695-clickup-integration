import json
import os
import requests
from requests import Request, Session
import warnings
import datetime
from dotenv import load_dotenv

load_dotenv()

s = Session() # speeds up the requests
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")

subteams = {
    "Fabrication": {"901104858222", "901101495836"},
    "Design+CAD": {"901101495833", "901104890072"},
    "Software": {"901101495817", "901104858222"},
    "Strategy+Scouting": {"901101497371"}
}

class task:
    def __init__(self, name, status, assignees, due_date):
        #print("name: ", name, "status: ", status, "assignees: ", assignees, "due: ", due_date)
        self.name = name
        self.status = status
        self.assignees = assignees
        self.due_date = datetime.date.fromtimestamp(int(due_date)/1000) if due_date else None

    def __str__(self):
        #return "task here!"
        return "* " + (f"({self.due_date}) " if self.due_date else "") + self.name

# finds the tasks from the cache.json file
def display_tasks(emails: set, statuses: set, subteam: str) -> str:
    print(subteam)
    if(len(emails) == 0):
        warnings.warn("User has empty email")
        return

    with open("cache.json", "r") as file:
        res = json.load(file)["tasks"]


    all_subteam_tasks = [task(x.get("name"), x.get("status"), x.get("assignees"), x.get("due_date")) for x in res if x["list"]["id"] in subteams[subteam] and len(x["assignees"]) == 0] if len(subteam) else []

    return [all_subteam_tasks, [task(x.get("name"), x.get("status"), x.get("assignees"), x.get("due_date")) for x in res if [z["email"] for z in x["assignees"] if z["email"] in emails]]]

# writes the current tasks to the cache.json file
def cache_tasks():
    display_url = "https://api.clickup.com/api/v2/team/9011117189/task"
    headers = {
        'Authorization': CLICKUP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.get(display_url, headers=headers)

    tasks = response.json()
    tasks_json = json.dumps(tasks, indent=4, sort_keys=True)

    with open("cache.json", "w") as file:
        file.write(tasks_json)
        print("cached")
