import bisect
from usefulNamedTuples import Bug
from findNewlineIndices import find_indices_of_new_lines
from timedFunction import timed
from stringAndFileFromPath import files_as_strings_from_path_gen
from changeInScopeLevel import change_in_scope_level
import os

@timed
def check_duplicate_ids(mod_path, output_file):
    bugs = []
    id_set = set()
    directories = [os.path.join("events"), os.path.join(mod_path, "common", "national_focus")]
    for path in directories:
        for contents, filename in files_as_strings_from_path_gen(path):
            for id_tag, line_number in duplicate_ids_gen(contents):
                if id_tag in id_set:
                    bugs += [Bug('Duplicate ID in scope', line_number + 1, filename)]
                else:
                    id_set.add(id_tag)

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')


def duplicate_ids_gen(string):
    endline_indices = find_indices_of_new_lines(string)
    index = 0
    try:
        while index < len(string):
            while string[index] != '{':
                index += 1
            scope_without_nested_contents = ''
            scope_level = 1
            start_index = index
            while scope_level > 0:
                index += 1
                scope_level += change_in_scope_level(string[index])
                if scope_level == 1:
                    scope_without_nested_contents += string[index]
            id_tag = find_contents_of_field(scope_without_nested_contents, 'id')
            if id_tag == '':
                pass
            else:
                line_number = bisect.bisect(endline_indices, start_index)
                yield id_tag, line_number
    except IndexError:
        pass


def find_contents_of_field(string, field_name):
    index = 0
    while index < len(string):
        next_id_index = string.find(field_name, index)
        if next_id_index == -1:
            return ''
        elif string[next_id_index-1] in ' \r\n\t':
            id_start = next_id_index + 2
            while not string[id_start].isalnum():
                id_start += 1
            id_end = id_start
            while not string[id_end] in ' \r\n\t}':
                id_end += 1
            return string[id_start:id_end]
        else:
            index = next_id_index + 1


