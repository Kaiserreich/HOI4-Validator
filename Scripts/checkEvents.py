import os
import bisect

from findNewlineIndices import find_indices_of_new_lines
from timedFunction import timed
from removeComments import remove_comments
from openFile import open_file


@timed
def check_events(mod_path, output_file):
    events_directory = '/events/'
    path = mod_path + events_directory
    for contents, filename in files_as_strings_from_path_gen(path):
        contents = remove_comments(contents)
        for event, start_line in events_gen(contents):
            if 'ai_chance' in event and event.count('option =') == 1:
                output_file.write("ai_chance present in event starting at " + str(start_line) + ' in ' + filename + ' but there is only one option.\n')
            if 'hidden = yes' not in event and 'picture =' not in event:
                output_file.write("No picture for event starting at " + str(start_line) + ' in ' + filename + '.\n')
            if 'hidden = yes' in event:
                if 'picture =' in event:
                    output_file.write("Hidden event at " + str(start_line) + ' in ' + filename + ' has a picture.\n')
                if 'title =' in event:
                    output_file.write(
                        "Hidden event at " + str(start_line) + ' in ' + filename + ' has a title.\n')
                if 'desc =' in event:
                    output_file.write("Hidden event at " + str(start_line) + ' in ' + filename + ' has a description.\n')
                if 'option =' in event:
                    output_file.write(
                        "Hidden event at " + str(start_line) + ' in ' + filename + ' has options.\n')


def files_as_strings_from_path_gen(path):
    for directory, subdirs, files in os.walk(path):
        for file in files:
            current_file = open_file(directory+file)
            contents = current_file.read()
            yield contents, file


def events_gen(string):
    search_terms = ['news_event', 'country_event']
    indices_of_newlines = find_indices_of_new_lines(string)
    index = -1
    while True:
        index = min([string.find(search_term, index + 1) for search_term in search_terms])
        # find returns -1 when nothing is found after the starting index
        if index != -1:
            start_index = index
            # if there is a bracket mismatch, just end the generator
            try:
                end_index = find_end_index(string, start_index)
            except IndexError:
                break
            event_body = string[start_index:end_index+1]
            # +1 since lines start at 1
            start_line = bisect.bisect(indices_of_newlines, start_index) + 1
            yield event_body, start_line
            index = end_index
        else:
            break


def find_end_index(string, start_index):
    potential_end_index = start_index + 1
    while string[potential_end_index] != '{':
        potential_end_index += 1
    scope_level = 1
    while scope_level != 0:
        potential_end_index += 1
        scope_level += change_in_scope_level(string[potential_end_index])
    return potential_end_index


def change_in_scope_level(char):
    if char == '{':
        return 1
    elif char == '}':
        return -1
    else:
        return 0
