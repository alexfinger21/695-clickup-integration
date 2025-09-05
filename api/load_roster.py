import json

# Loads the roster (barcode info, name, row, col, subteam, etc.) 
# Either from the google spreadsheet 
# Or local json (roster.json)

def load_roster(mypath, G_sheet_roster):
    try:
        with open(mypath + "roster.json", "r") as f:
            G_roster = json.load(f)

        print("Roster loaded from local file roster.json.  Delete to load from google.")
    except:
        G_roster = G_sheet_roster.get_all_records()
        print("Local file roster.json not found.  Roster loaded from google.")

        # write out local copy if needed
        #with open(mypath + "roster.json", "w") as f: 
            #f.write(json.dumps(G_roster, indent=4))

        # fixup numerics to strings for later comparisons
        for member in G_roster:
            member["BarcodeID"] = str(member["BarcodeID"])
            print(member["BarcodeID"])
            #member["StudentCell"] = str(member["StudentCell"])
            #member["ParentCell"] = str(member["ParentCell"])
    
    return G_roster