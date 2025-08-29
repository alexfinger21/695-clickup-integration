# Timeclock 
This is the main file that the scanner uses when logging in. It includes functionality like accessing student data from the student database, updating tasks from Clickup, and processing the actual scanner input. The actual API calls are processed by functions within the `api` folder/directory. 

This documentation will talk about how to properly setup your repository in order to actually run it, and how the program actually works.

**NOTE:** This documentation was made with vscode in mind, if you are using a different IDE keep this in mind.

## Installation and Setup
First off, you will want to clone the git repository in order to actually have access to the code:
1. Go to https://github.com/alexfinger21/695-clickup-integration where the project is located, you may need to log in to an account with access to the repository to see the code.
2. Click on the green **Code** button (you can't miss it, it's the only green button on the screen).
3. Make sure you have the **HTTPS** option selected and copy the link shown.
4. Open **File Explorer** (Windows) or your **file manager/terminal** (Linux), and navigate to the folder where you want the project to be saved.
	- *Right click, then click open with vscode* if on Windows
	- *Type `code <folder_path>`* if on Linux (Replace `<folder_path>` with the actual path)
5. In vscode terminal type `git clone <link_that_you_just_copied>` and run it
6. This should clone the git repository and you are ready to code.
7. ❗ If you weren't able to get the link this is the current link: https://github.com/alexfinger21/695-clickup-integration.git keep in mind that it may be updated/changed in the future.

Now make sure you are in the repository directory by typing `pwd` in the terminal. It should output something like `/home/meerkat/Documents/robotics/projects/repos/695-clickup-integration`. The most important part is the last part, it should match the name of the github repository.

If you aren't in a folder like this, you may need to go back to file explorer and open up the repository folder that was made by git clone.

Now it is time to install any requirements for the project. You will activate a venv which is just a virtual environment which stores all the libraries with the following code in the vscode terminal:
1. `python -m venv venv` -- Create a new folder called `venv` to store the virtual environment
2. If on windows: `venv\Scripts\activate`
3. If on Mac/Linux: `source venv/bin/activate`
4. If this worked your terminal prompt should look something like                               
	 `(venv) [meerkat@archlinux 695-clickup-integration]$`
 5. In order to install all libraries required for the project run `pip install -r requirements.txt`
 6. You may need to download some other libraries not listed in the requirements.txt like tkinter: `pip install tkinter`

Your venv is now complete, the only thing you need now is some files like `client_secret.json` and the `.env` which you can obtain from Coach John.

## `timeclock.py`
 









## Problems
api/load_roster.py - doesn't update json if there already is one, this means manually deleting the local json if there is one
in order to start updating

api/funcs.py - display_tasks() function - Won't display tasks if there are different emails in clickup and student sheet

timeclock.py - G_main.geometry("x_pixels", "y_pixels") what size is used on actual raspberry pi

timeclock.py - Loading infinitely on clockin:
- Mayer
- Amber
- Charlotte
- Eva
- Stella


