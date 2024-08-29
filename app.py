# dummy db
users = {
    "admin": "rev",
    "jerry": "123",
    "gerald": "screw-jerry"
}


if 'G_member' in locals():
    print("Signed in as" + G_member + ", if you need help type 'help'")
else:
    print("Signed in as *, if you need help type 'help'")

# process all input in the cli
def acceptInput():
    command = input()
    match command:
        case "help":
            print("Commands:\nmytasks - Display current assigned tasks\nsign out - Sign out of clickup")
            return True
        case "mytasks":
            print("Your tasks are")
            return True
        case "sign out":
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

def login():
    username = input("Username: ")
    pw = input("Password: ")

    if getUser(username, pw) == True:
        loggedIn()
    else:
        login()


def loggedIn():
    print('Enter "help" to view commands')
    while acceptInput():
        print("...")

var loginB = input("Login to ClickUp? (y/n)")

if loginB == "y" or loginB == "yes" or loginB == "Y" or loginB == "Yes" :
    username = input("Username: ")
    pw = input("Password: ")

    getUser(username, pw)
else: 
    print("Not logged in")


