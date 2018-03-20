# PDS-Validator
Home of the up and coming validator for Hearts of Iron 4, help is always welcome!

GUIDE by Roparex:

HOW TO USE:

if you have python installed, open a command line and run:
 start.py [Mod Directory]
Example:

 start.py C:\Users\ZankSucks\Documents\Paradox Interactive\Hearts of Iron IV\mod\Kaiserreich
 
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

Have fun coding!



