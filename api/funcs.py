import json
from urllib.request import Request, urlopen

def display_tasks(email: str, statuses: set) -> str:
    display_url = f"https://api.clickup.com/api/v2/list/901101497371/task?{'&'.join(['statuses[]=' + x.replace(' ', '+') for x in statuses])}&page=0"
    
    print(display_url)

    apiFINDReq = Request(
        display_url, 
        data=json.dumps({"test": True}).encode(), 
        method="GET",
        headers={"Authorization": "pk_14742653_2DD8K5CYR2LMRSZ7TWVE8POG2FB0EVKB"}
    ) #test if login required works

    res = urlopen(apiFINDReq)
    res = json.loads(res.read())["tasks"]
    print(res[0])

    res = [x.get("name")for x in res if email in x["assignees"]]
    print(res)
