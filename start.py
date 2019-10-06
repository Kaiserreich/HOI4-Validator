import os
import sys
import time
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
from checkFocus import check_for_missing_focus
from checkCores import check_for_missing_cores
from checkOOB import check_for_missing_OOB
from checkEvents import check_events
from checkEndlines import check_endlines
from checkGeneral import check_for_missing_General, create_general_list
from checkForEqualsNo import check_for_equals_no
from checkUnusedOOB import check_for_unused_OOB
from checkMissingLoc import check_for_missing_loc
from checkAliveCheck import check_alive_check
from checkMissingEquals import check_missing_equals
from checkDuplicateIds import check_duplicate_ids
from checkEventUsage import check_event_usage
from checkFlagUsage import check_flag_usage
from checkIdeaUsage import check_idea_usage
from checkMutallyExclusiveFocuses import check_mutually_exclusive_focuses
from kr_checkForNavalAviationTech import check_for_naval_aviation_tech
from checkOOBContents import check_OOB_Contents
from checkIdeologies import check_ideologies
from checkStates import check_states
from checkVpLoc import check_for_vp_loc
# output file initialisation

# functions go HERE

def start(mod_path, hoi4_path):
    t0 = time.time()
    print(dirName + '\\options.txt')
    optionsdict = {}
    settings_file = open('settings.txt', 'r', 'utf-8-sig')
    outputfile = 'validator.txt'
    for line in settings_file:
        if 'Output File:' in line and line.replace('Output File:', '') != '':
            outputfile = line.replace('Output File:', '')
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
    try:
        output_file = open(outputfile, 'w', 'utf-8-sig')
    except:
        output_file = open('validator.txt', 'w', 'utf-8-sig') #it'll default to doing this in the base folder if there's an issue in the way the output file location is specified
    if optionsdict["check_ideologies"]:
        check_ideologies(mod_path, optionsdict["uses_default_ideologies"], output_file)
    if optionsdict["check_missing_division_name_group"]:
        missing_divisions_names_group(mod_path, output_file, optionsdict["skip_unlock"])
    if optionsdict["check_for_old_generals"]:
        check_for_old_generals(mod_path, output_file)
    if optionsdict["check_for_name_lists"]:
        check_for_name_lists(mod_path, output_file)
    if optionsdict["check_for_brackets"]:
        check_brackets(mod_path, output_file)
    if optionsdict["check_for_double_locs"] or optionsdict["check_for_double_loc_spaces"]:
        check_for_double_locs(mod_path, output_file, bool(optionsdict["check_for_double_locs"]), bool(optionsdict["check_for_double_loc_spaces"]))
    if optionsdict["check_for_missing_gfx"]:
        check_for_missing_gfx(mod_path, output_file, hoi4_path)
    if optionsdict["check_for_missing_focus"]:
        check_for_missing_focus(mod_path, output_file)
    if optionsdict["check_for_missing_cores"]:
        check_for_missing_cores(mod_path, output_file)
    if optionsdict["check_for_missing_oobs"]:
        check_for_missing_OOB(mod_path, output_file)
    check_events(mod_path, output_file, optionsdict) #optionsdict is checked in the function, so no if for it
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
        check_for_missing_loc(mod_path, output_file, optionsdict)
    if optionsdict["check_for_alive_checks"]:
        check_alive_check(mod_path, output_file)
    if optionsdict["check_for_missing_equals"]:
        check_missing_equals(mod_path, output_file)
    if optionsdict["check_for_duplicate_ids"]:
        check_duplicate_ids(mod_path, output_file)
    if optionsdict["check_for_event_use"]:
        check_event_usage(mod_path, output_file)
    if optionsdict["check_flag_usage"]:
        check_flag_usage(mod_path, output_file)
    if optionsdict["check_idea_usage"]:
        check_idea_usage(mod_path, output_file)
    if optionsdict["check_mutually_exclusive_focuses"]:
        check_mutually_exclusive_focuses(mod_path, output_file)
    if optionsdict["check_naval_tech"]:
        check_for_naval_aviation_tech(mod_path, output_file)
    if optionsdict["check_states"]:
        check_states(mod_path, output_file)
    if optionsdict["check_vp_loc"]:
        check_for_vp_loc(mod_path, output_file, False)
    if optionsdict["check_kr_endo_vp_loc"]:
        check_for_vp_loc(mod_path, output_file, True)

    check_OOB_Contents(mod_path, output_file, optionsdict)#optionsdict is checked in the function, so no if for it
    t0 = time.time() - t0
    print("Total time taken: " + (t0*1000).__str__() + " ms")











