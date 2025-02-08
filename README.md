ClickUp get request for get tasks that are in progress for scouting and strategy list id 901101497371
https://api.clickup.com/api/v2/list/901101497371/task?statuses[]=in+progress&page=0

clickup put request to update task:
https://api.clickup.com/api/v2/task/86891yyef
body (json):
{
    "name": "test task",
    "description": "695 super duper",
    "status": "in progress",
    "priority": 1,
    "time_estimate": 8640000,
    "archived": false
}
