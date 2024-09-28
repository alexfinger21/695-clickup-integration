from api.api import display_tasks

def acceptInput():
    command = input()
    match command:
        case "help":
            print("Commands:\ndisplay\exit")
            return True
        case "display":
            print("Your tasks are")
            return True
        case "exit":
            print("Signing out of clickup")
            return False
        case _:
            print("Command not recognized")
            return True

# Dummy login 
def getUser(user, pw):
    match user:
        case "admin":
            if pw == "rev":
                return True
            else:
                print("Invalid Password")
                return False
        case "user":
            if pw == "pw":
                return True
            else: 
                print("Invalid password")
                return False
        case _:
            print("Invalid username")

username = input("Username: ")
pw = input("Password: ")

getUser(username, pw)

print('Enter "help" to view commands')
while acceptInput():
    print("...")
"""
