import json
import os
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
        return (f"({self.due_date}) " if self.due_date else "") + self.name

def display_tasks(emails: set, statuses: set, subteam: str) -> str:
    print(subteam)
    if(len(emails) == 0):
        warnings.warn("User has empty email")
        return

    display_url = f"https://api.clickup.com/api/v2/team/9011117189/task?{'&'.join(['statuses[]=' + x.replace(' ', '+') for x in statuses])}&lists[]={'&lists[]='.join(subteams[subteam])}&page=0"

    apiFINDReq = Request(
        "GET",
        display_url, 
        data=json.dumps({"test": True}).encode(), 
        headers={"Authorization": CLICKUP_API_KEY}
    ) #test if login required works
    apiFINDReq = apiFINDReq.prepare()

    res = s.send(apiFINDReq, 
         stream={}, 
         verify=True, 
         proxies=None, 
         cert=None, 
         timeout=None
    )

    res = json.loads(res.text)["tasks"]

    return [task(x.get("name"), x.get("status"), x.get("assignees"), x.get("due_date")) for x in res if [z["email"] for z in x["assignees"] if z["email"] in emails]]

