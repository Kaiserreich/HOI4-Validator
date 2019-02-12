# HOI4-Validator
Home of the validator for Hearts of Iron 4, help very much welcome!

How to use:

Open the validatorGUI.exe and fill in the blanks with the directory with your mod and the directory with Hoi4 on it and press run. After a few seconds another window will appear telling you it finished.
(Requires the latest .NET, should be autoinstalled on windows 10)

If you don't wanna use the GUI,open a command prompt in the same directory as the validator and use it like this:

validator.exe --Mod Location --HoI4 Location

Example:

validator.exe --C:\Users\ZankSucks\Documents\Paradox Interactive\Hearts of Iron IV\mod\Kaiserreich --C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV

Features can be activated or deactivated in options.txt

CURRENT FEATURES:

	Checks for divisions without namelists.
	
	Checks for tags whose namelists do not have names for garissons and militia.

	Checks for generals that use the pre-waking the tiger system. (Or, rather, checks for generals that have comments on them that say they use the pre-waking the tiger system)

	Checks for tags that lack namelists

	Checks to make sure that the right brackets are used, as well as that there is always an even number of brackets.

	Checks for locs that have been defined more than once

	Checks for missing graphics

	Checks for missing focuses

	Checks for states that do not have cores on them at game start

	Checks for OOBs that are referenced but don't exist

	Checks to make sure events have pictures

	Checks to make sure endlines are properly spaced

	Checks to make sure that generals referenced actually exist

	Produces a list of all general IDs currently in use

	Checks to see if = no is used in a place where that would cause an issue with a tooltip

	Checks for OOBs that are defined but not used.

	Checks for missing '='.

    Checks to make sure that nations that have certain naval techs have the prerequisite techs. (KR specific)
    
    Checks for templates in non-unlock OOBs without specified namelists
    
    Checks for units in OOBs without templates
    
    Checks for templates in OOBs without names
    
    Checks to make sure division templates in a OOB are defined before the units in that OOB
    
    Checks to make sure referenced ideologies are actually defined
	
	Checks to make sure VPs all have localization

	Checks to make sure all VP loc has a corresponding VP
 
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

py console_start.py --Mod Location --HoI4 Location 

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

When you add a feature, please remember to add it to the feature list in this document.

Have fun coding!



