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

username = input("Username: ")
print('Enter "help" to view commands')
while acceptInput():
    print("...")