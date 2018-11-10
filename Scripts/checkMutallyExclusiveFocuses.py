import os
import collections
from timedFunction import timed
from stringAndFileFromPath import files_as_strings_from_path_gen
from scopeGen import scope_gen
from fieldContentsGen import field_contents_gen
from usefulNamedTuples import Bug

Focus = collections.namedtuple('Focus', 'line_number file_name mutually_exclusive_with')

@timed
def check_mutually_exclusive_focuses(path, output_file):
    path = os.path.join(path, 'common', 'national_focus')
    focus_dict = {}
    for string, file in files_as_strings_from_path_gen(path):
        for focus, line_number in scope_gen(string, ['focus', 'shared_focus']):
            id, not_used = next(field_contents_gen(focus, 'id'))
            mutually_exclusive_focuses = []
            for mutually_exclusive, index in scope_gen(focus, ['mutually_exclusive']):
                for focus_id, index in field_contents_gen(mutually_exclusive, 'focus'):
                    mutually_exclusive_focuses.append(focus_id)
            focus = Focus(line_number, file, mutually_exclusive_focuses)
            focus_dict[id] = focus


    bugs = []
    for focus_id, focus in focus_dict.items():
        for mut_focus_id in focus.mutually_exclusive_with:
            try:
                if focus_id not in focus_dict[mut_focus_id].mutually_exclusive_with:
                    bugs.append(Bug('Focus is listed by another focus as mutually exclusive but does not list the other '
                                    'focus as mutually exclusive',
                                    focus_dict[mut_focus_id].line_number,
                                    focus_dict[mut_focus_id].file_name))
            except KeyError:
                pass

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')

