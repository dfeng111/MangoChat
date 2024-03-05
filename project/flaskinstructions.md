The following commands are made for bash (through vscode or wsl) but could also be run through powershell, if you have access to python through it. You can use WSL or git bash to use bash for this. Useful info at the end of this doc.


1. Go to the `flask` directory and run this command: 
<!---->
    python3 -m venv mangoflask

This directory is included in the .gitignore, since it should be installed separately per user.

2. Run the command:
<!--  -->
    source mangoflask/bin/activate

or 

    source mangoflask/Scripts/activate

or, if using powershell

    .\mangoflask\Scripts\Activate.ps1

This will bring you into the python virtual environment.

3. Install the project's dependencies by running: 
<!---->
    pip install -r requirements.txt

New packages can be installed/uninstalled with the following command:

    pip install/uninstall [names of packages separated by spaces]

If you decide the package you install is useful to the project and you use it, use this to update the requirements:

    pip freeze > requirements.txt


4. Run flask - this will run it so you can access it at localhost:3000 in your browser. 
<!---->
    flask run -h localhost -p 3000

NOTE: This doesn't seem to work since we made it into a module. You can run the server now with:

    python app.py

Ctrl-C will stop the server, and you can exit the container with:

    deactivate


WSL tip: your C drive is available under the /mnt/c/ folder.

Bash tip: to see the possible file options for a cd or cat command, hit tab twice. Once you've typed part of it, you can use tab again for completion.

General tip: Once you've chosen powershell, git bash, or wsl, stick with it. If you want to use another, you'll have to remove the mangoflask directory and remake it (which shouldn't take too long anyway)
If you determine that you've installed a package that we will use and will all need to have, you can export the new dependency list by running: 
