from urllib import Request

class task:
    def __task__(name, description, id):
        self.name = name
        self.description = description
        self.id = id
    def __str__(self):
        return f"{self.name}\n{self.description}"
    def changeStatus(self):
        apiFINDReq = Request(f"https://api.clickup.com/api/v2/task/{self.id}", data=json.dumps({
            "name": task,
            "status": status,
        }).encode(), method="POST")
        