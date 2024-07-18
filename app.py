def acceptInput():
    command = input()
    match command:
        case "help":
            print("Commands:\ndisplay")
            return True
        case "display":
            print("Your tasks are")
            return True
        case "exit":
            return False
        case _:
            print("Command not recognized")
            return True

def getUser(user, pw):
    match user:
        case "admin":
            if pw == "rev":
                return True
            else:
                return False
        case "user":
            if pw == "pw":
                return True
            else: 
                return False

username = input("Username: ")
pw = input("Password: ")

getUser(username, pw)

print('Enter "help" to view commands')
while acceptInput():
    print("...")