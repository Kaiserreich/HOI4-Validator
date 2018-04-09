import os
import sys

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


# output file initialisation

# functions go HERE

def start(mod_path, hoi4_path):
    output_file = open("validator.txt", 'w', 'utf-8-sig')
    missing_divisions_names_group(mod_path, output_file)
    check_for_old_generals(mod_path, output_file)
    check_for_name_lists(mod_path, output_file)
    check_brackets(mod_path, output_file)
    check_for_double_locs(mod_path, output_file)
    check_for_missing_gfx(mod_path, output_file, hoi4_path)











