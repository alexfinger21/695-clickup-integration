
users = {
    "admin": "rev",
    "jerry": "123",
    "gerald": "screw-jerry"
}

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
    if username in users:
        if pw == users[username]:
            print("Successful login")
            return True
        else:
            print("Invalid username or password")
            return False
    else:
        print("Invalid username or password")
        return False

username = input("Username: ")
pw = input("Password: ")

if getUser(username, pw) == True:
    print('Enter "help" to view commands')
    while acceptInput():
        print("...")
else:
    username = input("Username: ")
    pw = input("Password: ")

    getUser(username, pw)