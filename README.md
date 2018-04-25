# PDS-Validator
Home of the up and coming validator for Hearts of Iron 4, help is always welcome!

GUIDE by Roparex:

HOW TO USE:

Open the validatorGUI.exe and fill in the blanks with the directory with your mod and the directory with Hoi4 on it and press run. After a few seconds another window will appear telling you it finished.
(Requires the latest .NET, should be autoinstalled on windows 10)

If you don't wanna use the GUI,open a command prompt in the same directory as the validator and use it like this:

validator.exe --Mod Location --HoI4 Location

Example:

validator.exe --C:\Users\ZankSucks\Documents\Paradox Interactive\Hearts of Iron IV\mod\Kaiserreich --C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV


 
HOW TO CONTRIBUTE:

1. Pick an issue from the list, then go in the /Scripts folder and make a new script. Do a function that has as parameters the path to the mod and the output file. 
Example:

def kr_missing_militia_and_garrison (path, output_file):

And afterwards do whatever you need to do for the issue you're solving.

If the issue is specific to KR (Example, looking for militia divisions) please add a kr to the script file name and function name. Otherwise, don't do it. Example:

def missing_divisions_names_group (path, output_file):

2. In start.py, import your function like this:

from [FILE NAME] import [FUNCTION NAME]

Example:

from kr_missingMilitiaAndGarrison import kr_missing_militia_and_garrison

Then call the function with the parameters path and outputFile.
Example:

missing_divisions_names_group(path, outputFile)

Note: for debug purposes, use:

py console_start.py --C:\Users\sheehanmilesk\Documents\kaiserreich --C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV

to run the scripts


HOW TO BUILD STANDALONE EXECUTABLE:

1. Make sure that the 'pip' command works (if not, reinstall python and select pip to be installed)

example: py pip

2.use this command to install pyinstaller:

py pip install PyInstaller

3.check if pyinstaller now works:

pyinstaller --version

4.if no error occured, run script_exe.bat

You will now have the new validator.exe in the project root.

Try and do this before every push, so we always have the latest.exe for our users.

Have fun coding!



