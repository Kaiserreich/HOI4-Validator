import sys
import os
from codecs import open

dirName = os.path.dirname(__file__)
sys.path.append(dirName + "\\Scripts")

# imports go HERE
from missingDivisionNamesGroup import missing_divisions_names_group
from kr_missingMilitiaAndGarrison import kr_missing_militia_and_garrison
from kr_checkForOldGenerals import kr_check_for_old_generals

# Creating the path for the Mod
ok = 0
path = sys.argv[1]
for string in sys.argv:
    if ok < 2:
        ok += 1
    else:
        path += ' ' + string

# output file initialisation
outputFile = open("validator.txt", 'w', 'utf-8-sig')

# functions go HERE
missing_divisions_names_group(path, outputFile)
kr_missing_militia_and_garrison(path, outputFile)
kr_check_for_old_generals(path, outputFile)











