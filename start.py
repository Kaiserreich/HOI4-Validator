import os
import sys
import time
from codecs import open
dirName = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirName + "\\Scripts")

# imports go HERE
from openFile import open_file
from missingDivisionNamesGroup import missing_divisions_names_group
from checkForOldGenerals import check_for_old_generals
from checkForNameLists import check_for_name_lists
from checkBrackets import check_brackets
from checkForDoubleLocs import check_for_double_locs
from checkGFX import check_for_missing_gfx
from checkFocus import check_for_missing_focus
from checkCores import check_for_missing_cores
from checkOOB import check_for_missing_OOB
from checkEvents import check_events
from checkEndlines import check_endlines
from checkGeneral import check_for_missing_General, create_general_list
from checkForEqualsNo import check_for_equals_no
from checkUnusedOOB import check_for_unused_OOB
from checkMissingLoc import check_for_missing_loc


# output file initialisation

# functions go HERE

def start(mod_path, hoi4_path):
    t0 = time.time()
    print(dirName + '\\options.txt')
    optionsdict = {}
    options_file = open('options.txt', 'r', 'utf-8-sig')
    for line in options_file:
        #this checks through the options file to see if a given line is an option. If so, it checks the
        if ('#' in line) == False:
            line = line.strip()
            #print(line)
            if line != 'empty' and line != '':
                linelist = line.split(' = ')
                if linelist[1].strip() == 'yes':
                    optionsdict[linelist[0].strip()] = True
                else:
                    optionsdict[linelist[0].strip()] = False
    options_file.close()
    output_file = open("validator.txt", 'w', 'utf-8-sig')
    if optionsdict["check_missing_division_name_group"]:
        missing_divisions_names_group(mod_path, output_file)
    if optionsdict["check_for_old_generals"]:
        check_for_old_generals(mod_path, output_file)
    if optionsdict["check_for_name_lists"]:
        check_for_name_lists(mod_path, output_file)
    if optionsdict["check_for_brackets"]:
        check_brackets(mod_path, output_file)
    if optionsdict["check_for_double_locs"]:
        check_for_double_locs(mod_path, output_file)
    if optionsdict["check_for_missing_gfx"]:
        check_for_missing_gfx(mod_path, output_file, hoi4_path)
    if optionsdict["check_for_missing_focus"]:
        check_for_missing_focus(mod_path, output_file)
    if optionsdict["check_for_missing_cores"]:
        check_for_missing_cores(mod_path, output_file)
    if optionsdict["check_for_missing_oobs"]:
        check_for_missing_OOB(mod_path, output_file)
    if optionsdict["check_events"]:
        check_events(mod_path, output_file)
    if optionsdict["check_endlines"]:
        check_endlines(mod_path, output_file)
    if optionsdict["check_generals"]:
        check_for_missing_General(mod_path, output_file)
    if optionsdict["list_general_ids"]:
        create_general_list(mod_path, output_file)
    if optionsdict["check_for_equals_no"]:
        check_for_equals_no(mod_path, output_file)
    if optionsdict["check_for_unused_oobs"]:
        check_for_unused_OOB(mod_path, output_file)
    if optionsdict["check_for_missing_loc"]:
        check_for_missing_loc(mod_path, output_file)
    t0 = time.time() - t0
    print("Total time taken: " + (t0*1000).__str__() + " ms")











