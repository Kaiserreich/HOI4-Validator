import bisect
import collections

from changeInScopeLevel import change_in_scope_level
from findNewlineIndices import find_indices_of_new_lines
from stringAndFileFromPath import files_as_strings_from_path_gen
from timedFunction import timed

Bug = collections.namedtuple('Bug', 'description line filename')


@timed
def check_events(mod_path, output_file):

    def events_gen(string):

        def find_end_index(string, start_index):
            potential_end_index = start_index + 1
            while string[potential_end_index] != '{':
                potential_end_index += 1
            scope_level = 1
            while scope_level != 0:
                potential_end_index += 1
                scope_level += change_in_scope_level(string[potential_end_index])
            return potential_end_index

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
                event_body = string[start_index:end_index + 1]
                # +1 since lines start at 1
                start_line = bisect.bisect(indices_of_newlines, start_index) + 1
                yield event_body, start_line
                index = end_index
            else:
                break

    bugs = []
    events_directory = '/events/'
    path = mod_path + events_directory
    for contents, filename in files_as_strings_from_path_gen(path):
        for event, start_line in events_gen(contents):
            if 'ai_chance' in event and event.count('option =') == 1:
                bugs.append(Bug('\"ai_chance\" with only one option in event', start_line, filename))
            if 'hidden = yes' not in event:
                if 'picture =' not in event:
                    bugs.append(Bug('No picture for event', start_line, filename))
                if 'title =' not in event:
                    bugs.append(Bug('No title for event', start_line, filename))
                if 'desc =' not in event:
                    bugs.append(Bug('No description for event', start_line, filename))
                if 'option =' not in event:
                    bugs.append(Bug('No options for event', start_line, filename))
                if 'load_oob' in event and 'custom_effect_tooltip' not in event:
                    bugs.append(Bug('\"load_oob\" is an effect but there is no \"custom_effect_tooltip\" in event', start_line, filename))
            if 'hidden = yes' in event:
                if 'picture =' in event:
                    bugs.append(Bug('Picture in hidden event', start_line, filename))
                if 'title =' in event:
                    bugs.append(Bug('Title in hidden event', start_line, filename))
                if 'desc =' in event:
                    bugs.append(Bug('Description in hidden event', start_line, filename))
                if 'option =' in event:
                    bugs.append(Bug('Options in hidden event', start_line, filename))

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
