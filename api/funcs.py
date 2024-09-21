import json
from requests import Request, Session
import warnings

s = Session() # speeds up the requests

def display_tasks(emails: set, statuses: set) -> str:
    if(len(emails) == 0):
        warnings.warn("User has empty email")
        return

    display_url = f"https://api.clickup.com/api/v2/list/901101497371/task?{'&'.join(['statuses[]=' + x.replace(' ', '+') for x in statuses])}&page=0"

    
    print(display_url)

    apiFINDReq = Request(
        "GET",
        display_url, 
        data=json.dumps({"test": True}).encode(), 
        headers={"Authorization": "pk_14742653_2DD8K5CYR2LMRSZ7TWVE8POG2FB0EVKB"}
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
    return [x.get("name") for x in res if [z["email"] for z in x["assignees"] if z["email"] in emails]]

