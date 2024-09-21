import json
from urllib.request import Request, urlopen
import warnings

def display_tasks(emails: set, statuses: set) -> str:
    if(len(emails) == 0):
        warnings.warn("User has empty email")
        return
    display_url = f"https://api.clickup.com/api/v2/list/901101497371/task?{'&'.join(['statuses[]=' + x.replace(' ', '+') for x in statuses])}&page=0"
    
    print(display_url)

    apiFINDReq = Request(
        display_url, 
        data=json.dumps({"test": True}).encode(), 
        method="GET",
        headers={"Authorization": "pk_14742653_2DD8K5CYR2LMRSZ7TWVE8POG2FB0EVKB"}
    ) #test if login required works

    tasks = urlopen(apiFINDReq)
    tasks = json.loads(tasks.read())["tasks"]
    print(tasks[0])

    res = []

    for x in res:
        for a in x["assignees"]:
            if(emails.has(a)):
                res.append(x.get("name"))
    print(res)
