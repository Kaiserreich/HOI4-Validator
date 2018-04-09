import sys
import os
from codecs import open

dirName = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirName + "\\Scripts")

# imports go HERE
from missingDivisionNamesGroup import missing_divisions_names_group
from checkForOldGenerals import check_for_old_generals
from checkForNameLists import check_for_name_lists
from checkBrackets import check_brackets
from checkForDoubleLocs import check_for_double_locs
from checkGFX import check_for_missing_gfx

# Creating the path for the Mod
ok = 0
cpath = sys.argv[1]

for string in sys.argv:
    if ok < 2:
        ok += 1
    else:
        cpath += ' ' + string
        
path = cpath.split("--")[1].strip()
hoi4_path = cpath.split("--")[2].strip()

# output file initialisation
outputFile = open("validator.txt", 'w', 'utf-8-sig')

# functions go HERE

#missing_divisions_names_group(path, outputFile)
#check_for_old_generals(path, outputFile)
#check_for_name_lists(path, outputFile)
#check_brackets(path, outputFile)
#check_for_double_locs(path, outputFile)
check_for_missing_gfx(path, outputFile, hoi4_path)

print ('The validator finished, the output file should be at ' + os.path.abspath(outputFile.name))










