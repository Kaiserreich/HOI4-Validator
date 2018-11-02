import bisect

from stringAndFileFromPath import files_as_strings_from_path_gen
from findNewlineIndices import find_indices_of_new_lines
from changeInScopeLevel import change_in_scope_level
from usefulNamedTuples import Bug
from timedFunction import timed
import os

@timed
def check_alive_check(path, output_file):
    path = os.path.join(path, "events")
    for string, filename in files_as_strings_from_path_gen(path):
        for bug in missing_alive_check_gen(string, filename):
            output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')


def missing_alive_check_gen(string, filename):

    def find_start_index(string, index):
        potential_start_index = index
        scope_level = 1
        while scope_level != 0:
            potential_start_index -= 1
            scope_level -= change_in_scope_level(string[potential_start_index])
        return potential_start_index

    def find_end_index(string, index):
        potential_end_index = index
        scope_level = 1
        while scope_level != 0:
            potential_end_index += 1
            scope_level += change_in_scope_level(string[potential_end_index])
        return potential_end_index

    search_terms = ['diplomatic_relation']
    indices_of_newlines = find_indices_of_new_lines(string)
    index = -1
    while True:
        index = min([string.find(search_term, index + 1) for search_term in search_terms])
        # find returns -1 when nothing is found after the starting index
        if index != -1:
            start_line = bisect.bisect(indices_of_newlines, index) + 1
            enclosed_start = string.find('{', index)
            enclosed_end = find_end_index(string, enclosed_start)
            enclosed_scope = string[enclosed_start:enclosed_end + 1]
            try:
                start_index = find_start_index(string, index)
                end_index = find_end_index(string, index)
            except IndexError:
                yield Bug('\"diplomatic_relation\" effect has no check that subject is alive', start_line, filename)
                break
            if string[start_index-5:start_index] == 'if = ':
                enclosing_scope = string[start_index:end_index + 1]
                if 'country_exists' in enclosing_scope:
                    check_index = enclosing_scope.find('country_exists')
                    subject_of_check = enclosing_scope[check_index+17:check_index+20]
                    effect_index = enclosed_scope.find('country')
                    subject_of_effect = enclosed_scope[effect_index+10:effect_index+13]
                    if subject_of_effect != subject_of_check:
                        yield Bug('\"diplomatic_relation\" checks for the wrong country', start_line, filename)
                else:
                    yield Bug('\"diplomatic_relation\" effect has no check that subject is alive', start_line, filename)
            else:
                yield Bug('\"diplomatic_relation\" effect has no check that subject is alive', start_line, filename)
            index = end_index
        else:
            break
