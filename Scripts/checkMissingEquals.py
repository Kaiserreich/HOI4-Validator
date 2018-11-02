from timedFunction import timed
from stringAndFileFromPath import files_as_strings_from_path_gen
from usefulNamedTuples import Bug
import os

@timed
def check_missing_equals(mod_path, output_file):
    bugs = []
    directories = [os.path.join(mod_path, 'events'), os.path.join(mod_path, 'common', 'national_focus'), os.path.join(mod_path, 'interface'), os.path.join(mod_path, 'history')]
    for directory in directories:
        for contents, filename in files_as_strings_from_path_gen(directory):
            if "credits.txt" not in filename:
                bugs += [bug for bug in missing_equals_gen(contents, filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')


def missing_equals_gen(string, filename):
    lines = string.split('\n')
    for i, line in enumerate(lines):
        index = 0
        while index < len(line):
            try:
                while not line[index].isalnum():
                    index += 1
                while not line[index].isspace() and line[index] not in '=<>':
                    index += 1
                equals_found = False
                while not line[index].isalnum() and line[index] not in '{\"':
                    if line[index] in '<>=':
                        equals_found = True
                    index += 1
                if not equals_found:
                    if not is_a_list(line, index):
                        yield Bug('Missing \"=\"', i+1, filename)
                if line[index] == '{':
                    pass
                elif line[index] == '\"':
                    end_of_string_found = False
                    while not end_of_string_found:
                        index += 1
                        if line[index] == '\"' and line[index-1] != '\\':
                            end_of_string_found = True
                    while line[index] not in ' \t':
                        index += 1
                else:
                    while line[index] != ' ':
                        index += 1
            except IndexError:
                pass


def is_a_list(line, index):
    leading_enclosure_index = index - 1
    while leading_enclosure_index > 0 and line[leading_enclosure_index] != '{':
        leading_enclosure_index -= 1
    trailing_enclosure_index = index
    while trailing_enclosure_index < len(line) and line[trailing_enclosure_index] != '}':
        trailing_enclosure_index += 1
    list_body = line[leading_enclosure_index+1:trailing_enclosure_index]
    if '=' in list_body:
        return False
    if is_a_list_of_numbers(list_body):
        return True
    if is_a_list_of_strings(list_body):
        return True
    if is_a_list_of_directions(list_body):
        return True
    if is_traits(line, leading_enclosure_index):
        return True
    return False


def is_traits(line, index):
    name_end_index = index - 1
    try:
        while not line[name_end_index].isalpha():
            name_end_index -= 1
        if line[name_end_index-5:name_end_index+1] == 'traits':
            return True
        else:
            return False
    except IndexError:
        return False


def is_a_list_of_directions(list_body):
    valid_directions = ['left', 'middle', 'right']
    strings = list_body.split(' ')
    is_a_list_of_directions = True
    for string in strings:
        if len(string) > 0:
            if string not in valid_directions:
                is_a_list_of_directions = False
    return is_a_list_of_directions


def is_a_list_of_numbers(list_body):
    is_a_list_of_numbers = True
    for char in list_body:
        if char.isalpha():
            is_a_list_of_numbers = False
    return is_a_list_of_numbers


def is_a_list_of_strings(list_body):
    strings = list_body.split(' ')
    is_a_list_of_strings = True
    for string in strings:
        if len(string) > 0:
            if string[0] != '\"' or string[-1] != '\"':
                is_a_list_of_strings = False
    return is_a_list_of_strings
