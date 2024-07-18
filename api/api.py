from urllib import Request

def display_tasks(user: str) -> str:
    display_url = "https://api.clickup.com/api/v2/list/901101497371/task?statuses[]=in+progress&page=0"
    #apiFINDReq = Request("http://127.0.0.1:8080/api/find", data=json.dumps({"test": True}).encode(), method="POST") #test if login required works
    
