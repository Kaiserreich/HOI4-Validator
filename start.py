import os
import sys
import time
#import memory_profiler
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
from Scripts.PDSObject import PDSFocusTree
import pathos
import pickle
import statistics

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

def preparse_focuses(directory, preparsed_focuses_dict, focus_tree_properties_dict, pool):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    results = pool.map(lambda x: preparse_focus_file(x), files)
    #handle country
    for dct in results:
        if dct:
            if dct[0]:
                for key, value in dct[0].items():
                    preparsed_focuses_dict[key].extend(value)
            if dct[1]:
                for key, value in dct[1].items():
                    focus_tree_properties_dict[key] = value

def parse_focuses(preparsed_focuses_dict, focuses_dict, focus_tree_properties_dict, focus_trees_dict, pool):
    for key, value in preparsed_focuses_dict.items():
        results = pool.map(lambda x: parse_focus(key, x), value)
        for tpl in results:
            for key, value in tpl[0].items():
                focuses_dict[key] = value
            for key, value in tpl[1].items():
                if not key == 'shared_focus':
                    if not key in focus_trees_dict:
                        Logger.log("%s %s" % (key, str(value)))
                        focus_trees_dict[key] = PDSFocusTree(key, focus_tree_properties_dict[key][0], focus_tree_properties_dict[key][1], focus_tree_properties_dict[key][2])
                        focus_trees_dict[key].shared_focuses = focus_tree_properties_dict[key][3]
                    focus_trees_dict[key].focuses[value[0].focus_id] = value[0]

# functions go HERE

def find_children(focus, focus_dictionary):
    if not focus:
        return
    children = set()
    new_children = set()
    for f in focus_dictionary.values():
        if f.prerequisite:
            for prereq_list in f.prerequisite:
                for prereq in prereq_list:
                    if prereq == focus.focus_id:
                        children.add(f)
    for f in children:
        new_children = new_children.union(find_children(f, focus_dictionary))
    children = children.union(new_children)
    return children

def count_focuses(days_multiplier = 7):
    fcs_list = []

    for key, value in global_vars.FOCUS_TREES_DICT.items():
        shared_focuses = set()
        for shared_focus_id in value.shared_focuses:
            shared_focuses = shared_focuses.union(find_children(global_vars.FOCUSES_DICT[shared_focus_id], global_vars.FOCUSES_DICT))
        total_cost_set = set(value.focuses.values()).union(shared_focuses)
        total_cost = 0
        for fcs in total_cost_set:
            total_cost += fcs.cost
        fcs_list.append((key, len(value.focuses) + len(shared_focuses), total_cost*days_multiplier, len(shared_focuses)))
    
    fcs_list = sorted(fcs_list, key=lambda x: x[2], reverse=True)
    total_cost = 0
    for item in fcs_list:
        total_cost += item[2]
        Logger.log("%s: %s focuses (%g days | %.3g years, %.3g average), including %s shared" % (item[0], str(item[1]), item[2], item[2]/365, item[2]/item[1], str(item[3])))
    Logger.log("Total: %s focuses (%g days | %.3g years, %.3g average) in %s focus trees" % (str(len(global_vars.FOCUSES_DICT)), total_cost, total_cost/365, total_cost/len(global_vars.FOCUSES_DICT), str(len(global_vars.FOCUS_TREES_DICT))))

def count_civ_mil_factories_in_focuses():
    fcs_list = []
    total_civ = 0
    total_mil = 0

    for key, value in global_vars.FOCUS_TREES_DICT.items():
        shared_focuses = set()
        for shared_focus_id in value.shared_focuses:
            shared_focuses = shared_focuses.union(find_children(global_vars.FOCUSES_DICT[shared_focus_id], global_vars.FOCUSES_DICT))
        total_set = set(value.focuses.values()).union(shared_focuses)
        civ = 0
        mil = 0
        for fcs in total_set:
            if fcs.completion_reward:
                rtrn_tuple = get_added_civ_mil_factories(fcs.completion_reward)
                civ += rtrn_tuple[0]
                mil += rtrn_tuple[1]
        total_civ += civ
        total_mil += mil
        fcs_list.append((key, len(value.focuses) + len(shared_focuses), civ, mil))
    
    fcs_list = sorted(fcs_list, key=lambda x: x[3] + x[2], reverse=True)
    for item in fcs_list:
        Logger.log("%s: %d factories (%d CIV %d MIL)" % (item[0], item[3]+item[2], item[2], item[3]))
    Logger.log("Total: %d focuses giving %d factories (%d CIV %d MIL) in %d focus trees" % (len(global_vars.FOCUSES_DICT), total_civ+total_mil, total_civ, total_mil, len(global_vars.FOCUS_TREES_DICT)))

def get_total_tech_bonus_value_in_focuses():
    fcs_list = []
    total_value = 0
    total_uses = 0

    for key, value in global_vars.FOCUS_TREES_DICT.items():
        shared_focuses = set()
        for shared_focus_id in value.shared_focuses:
            shared_focuses = shared_focuses.union(find_children(global_vars.FOCUSES_DICT[shared_focus_id], global_vars.FOCUSES_DICT))
        total_set = set(value.focuses.values()).union(shared_focuses)
        tb_value = 0
        uses = 0
        for fcs in total_set:
            if fcs.completion_reward:
                rtrn_tuple = get_total_tech_bonus_value(fcs.completion_reward)
                tb_value += rtrn_tuple[0]
                uses += rtrn_tuple[1]
        total_value += tb_value
        total_uses += uses
        fcs_list.append((key, len(value.focuses) + len(shared_focuses), tb_value, uses))
    
    fcs_list = sorted(fcs_list, key=lambda x: x[2], reverse=True)
    for item in fcs_list:
        Logger.log("%s: %d uses with a total value of %d" % (item[0], item[3], item[2]))
    Logger.log("Total: %d focuses giving %d uses with a total value of %d in %d focus trees" % (len(global_vars.FOCUSES_DICT), total_uses, total_value, len(global_vars.FOCUS_TREES_DICT)))


def find_in_nested(nested, v):
    for element in nested:
        if hasattr(element, "__iter__") and not isinstance(element, str):
            result = find_in_nested(element, v)
            if result:
                return result
        elif element == v:
            return nested
    return False

def findall_in_nested(nested, v):
    results = []
    for element in nested:
        if hasattr(element, "__iter__") and not isinstance(element, str):
            results.append(find_in_nested(element, v))
        elif element == v:
            results.append(nested)
    return results


def get_added_civ_mil_factories(effect_block):
    civ_factories = 0
    mil_factories = 0
    results = findall_in_nested(effect_block, 'add_building_construction')
    for result in results:
        if result:
            level_block = find_in_nested(result, 'level')
            level = 0
            if level_block:
                level = float(level_block[2])
            type_block = find_in_nested(result, 'type')
            if type_block:
                if type_block[2] == 'industrial_complex':
                    civ_factories += level
                elif type_block[2] == 'arms_factory':
                    mil_factories += level
    return (civ_factories, mil_factories)

def get_total_tech_bonus_value(effect_block):
    value = 0
    total_uses = 0
    results = findall_in_nested(effect_block, 'add_tech_bonus')
    for result in results:
        if result:
            uses_block = find_in_nested(result, 'uses')
            if uses_block:
                uses = float(uses_block[2])
            else:
                uses = 1
            total_uses += uses
            bonus_block = find_in_nested(result, 'bonus')
            if bonus_block:
                value += float(bonus_block[2]) * uses
    return (value, total_uses)

def start(mod_path, hoi4_path):
    '''t0 = time.time()
    pool = pathos.multiprocessing.Pool(8)

    
    preparse_ideas(
        os.path.join(mod_path, "common", "ideas"), global_vars.PREPARSED_IDEAS_DICT, pool
    )
    parse_ideas(
        global_vars.PREPARSED_IDEAS_DICT, global_vars.IDEAS_DICT, global_vars.IDEA_SLOTS_DICT, pool
    )
    
    parse_idea_file(
        os.path.join(mod_path, "common", "ideas", "_KR_Political_ideas.txt"), IDEAS_DICT, IDEA_SLOTS_DICT
    )
    
    preparse_focuses(
        os.path.join(mod_path, "common", "national_focus"), global_vars.PREPARSED_FOCUSES_DICT, global_vars.FOCUS_TREE_PROPERTIES_DICT, pool
    )
    parse_focuses(
        global_vars.PREPARSED_FOCUSES_DICT, global_vars.FOCUSES_DICT, global_vars.FOCUS_TREE_PROPERTIES_DICT, global_vars.FOCUS_TREES_DICT, pool
    )
    pool.close()
    pool.join()
    t0 = time.time() - t0
    Logger.log("Total time taken: " + (t0*1000).__str__() + " ms")'''
    
    with open(os.path.join(mod_path, 'FOCUSES_DICT.pickle'), 'rb') as handle:
        global_vars.FOCUSES_DICT = pickle.load(handle)
    with open(os.path.join(mod_path, 'FOCUS_TREES_DICT.pickle'), 'rb') as handle:
        global_vars.FOCUS_TREES_DICT = pickle.load(handle)

    get_total_tech_bonus_value_in_focuses()

    #count_focuses()


    #with open(os.path.join(mod_path, 'FOCUSES_DICT.pickle'), 'wb') as handle:
    #    pickle.dump(global_vars.FOCUSES_DICT, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #with open(os.path.join(mod_path, 'FOCUS_TREES_DICT.pickle'), 'wb') as handle:
    #    pickle.dump(global_vars.FOCUS_TREES_DICT, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    start(os.path.join("Tests", "Kr"), None)










