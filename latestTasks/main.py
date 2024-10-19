import json
import os
import requests
from requests import Request, Session
import math
import datetime
import time
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    s = Session()

    statuses = ["in progress", "to do", "priority", "block"]
    status_str = '&'.join(statuses).replace(' ', '+')

    CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
    print("date from (YYYY-MM-DD):")
    dt = datetime.datetime.fromisoformat(str(input()))

    display_url = f"https://api.clickup.com/api/v2/team/9011117189/task?date_created_gt={math.floor(time.mktime(dt.timetuple())*1000)}&{status_str}&page=0"

    headers = {
        'Authorization': CLICKUP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.get(display_url, headers=headers)

    tasks = [x["name"] for x in response.json()["tasks"]]
    for t in tasks:
        print(t)

