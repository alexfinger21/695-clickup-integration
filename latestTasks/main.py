import json
import os
import requests
from requests import Request, Session
import math
import datetime
import time
from dotenv import load_dotenv
from operator import itemgetter 

if __name__ == "__main__":
    load_dotenv()
    s = Session()

    statuses = ["in progress", "to do", "priority", "block"]
    status_str = '&'.join(statuses).replace(' ', '+')

    CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
    print("date from (YYYY-MM-DD):")
    inp = str(input())
    dt = datetime.datetime.fromisoformat(inp) if inp else datetime.datetime.fromtimestamp(time.time()-60*60*24*7)

    display_url = f"https://api.clickup.com/api/v2/team/9011117189/task?date_created_gt={math.floor(time.mktime(dt.timetuple())*1000)}&{status_str}&page=0"

    headers = {
        'Authorization': CLICKUP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.get(display_url, headers=headers)

    tasks = response.json()["tasks"]
    task_subteams = dict()

    tasks.sort(key=lambda x: x["folder"]["name"])
    tasks.sort(key=lambda x: x["creator"]["username"])

    for t in tasks:
        st = t["folder"]["name"]
        if (not task_subteams.get(st)):
            task_subteams[st] = [f'{t["name"]} | Date created: {datetime.datetime.fromtimestamp(int(t["date_created"])/1000).strftime("%m/%d/%Y")} | Status: {t["status"]["status"]} | Sub-team: {st} | Creator: {t["creator"]["username"]}']
        else:
            task_subteams[st].append(f'{t["name"]} | Date created: {datetime.datetime.fromtimestamp(int(t["date_created"])/1000).strftime("%m/%d/%Y")} | Status: {t["status"]["status"]} | Sub-team: {st} | Creator: {t["creator"]["username"]}')

    for t in task_subteams.keys():
        print(t + ':')
        for task in task_subteams[t]:
            print(task)
        print()
