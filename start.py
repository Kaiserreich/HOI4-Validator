import os
import sys
import time
import memory_profiler
import multiprocessing, logging
mpl = multiprocessing.log_to_stderr()
mpl.setLevel(logging.INFO)
from codecs import open

dirName = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dirName, "Scripts"))

# imports go HERE
'''
from missingDivisionNamesGroup import missing_divisions_names_group
from checkForOldGenerals import check_for_old_generals
from checkForNameLists import check_for_name_lists
from checkBrackets import check_brackets
from checkForDoubleLocs import check_for_double_locs
from checkGFX import check_for_missing_gfx
from checkFocus import check_for_missing_focus
from checkCores import check_for_missing_cores
'''
import Scripts.global_vars as global_vars
from Scripts.validator_logging import LOGGER as Logger
from Scripts.parsePDS import preparse_idea_file, parse_idea, preparse_focus_file, parse_focus
import pathos

# output file initialisation
def preparse_ideas(directory, preparsed_ideas_dict, pool):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    results = pool.map(lambda x: preparse_idea_file(x), files)
    for dct in results:
        if dct:
            for key, value in dct.items():
                preparsed_ideas_dict[key].extend(value)

def parse_ideas(preparsed_ideas_dict, ideas_dict, idea_slots_dict, pool):
    results = pool.map(lambda x: parse_idea(x[0], x[1]), preparsed_ideas_dict.items())
    for tpl in results:
        for key, value in tpl[0].items():
            ideas_dict[key] = value
        for key, value in tpl[1].items():
            idea_slots_dict[key].extend(value)

def preparse_focuses(directory, preparsed_focuses_dict, pool):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    results = pool.map(lambda x: preparse_focus_file(x), files)
    #handle country
    for dct in results:
        if dct:
            for key, value in dct.items():
                preparsed_focuses_dict[key].extend(value)

def parse_focuses(preparsed_focuses_dict, focuses_dict, focus_trees_dict, pool):
    for key, value in preparsed_focuses_dict.items():
        results = pool.map(lambda x: parse_focus(key, x), value)
        for tpl in results:
            for key, value in tpl[0].items():
                focuses_dict[key] = value
            for key, value in tpl[1].items():
                focus_trees_dict[key].extend(value)

# functions go HERE

def start(mod_path, hoi4_path):
    t0 = time.time()
    pool = pathos.multiprocessing.Pool(8)

    '''
    preparse_ideas(
        os.path.join(mod_path, "common", "ideas"), global_vars.PREPARSED_IDEAS_DICT, pool
    )
    parse_ideas(
        global_vars.PREPARSED_IDEAS_DICT, global_vars.IDEAS_DICT, global_vars.IDEA_SLOTS_DICT, pool
    )
    
    parse_idea_file(
        os.path.join(mod_path, "common", "ideas", "_KR_Political_ideas.txt"), IDEAS_DICT, IDEA_SLOTS_DICT
    )'''
    preparse_focuses(
        os.path.join(mod_path, "common", "national_focus"), global_vars.PREPARSED_FOCUSES_DICT, pool
    )
    parse_focuses(
        global_vars.PREPARSED_FOCUSES_DICT, global_vars.FOCUSES_DICT, global_vars.FOCUS_TREES_DICT, pool
    )
    pool.close()
    pool.join()
    t0 = time.time() - t0
    print("Total time taken: " + (t0*1000).__str__() + " ms")

start(os.path.join("Tests", "Kr"), None)










