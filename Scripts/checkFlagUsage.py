import collections

from timedFunction import timed
from checkEvents import scope_gen
from stringAndFileFromPath import files_as_strings_from_path_gen
from checkEvents import Bug
from checkDuplicateIds import field_contents_gen

Flag = collections.namedtuple('Flag', 'name start_line filename')


@timed
def check_flag_usage(mod_path, output_file):
    global_flags_set = []
    global_flags_modified = []
    global_flags_checked = []
    global_flags_cleared = []

    flag_set_directories = ['//events', '//common//decisions', '//common//scripted_effects',
                            '//common//national_focuses', '//history//countries', '//common//on_actions']
    paths = [mod_path + directory for directory in flag_set_directories]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for flag, start_line in field_contents_gen(contents, 'set_global_flag'):
                if flag not in global_flags_set:
                    global_flags_set += [Flag(flag, start_line, filename)]
            for modify_flag, start_line in scope_gen(contents, ['modify_global_flag']):
                flag, line_offset = next(field_contents_gen(modify_flag, 'flag'))
                if flag not in global_flags_modified:
                    global_flags_modified += [Flag(flag, start_line+line_offset-1, filename)]
            for flag, start_line in field_contents_gen(contents, 'clr_global_flag'):
                if flag not in global_flags_cleared:
                    global_flags_cleared += [Flag(flag, start_line, filename)]

    flag_checking_directories = ['//events', '//common//decisions', '//common//scripted_triggers',
                                 '//common//scripted localisation', '//common//national_focuses',
                                 '//common//on_actions', '//common//ai_peace', '//common//ai_strategy',
                                 '//common//ai_strategy_plans', '//common//autonomous_states', '//common//ideas',
                                 '//common//technologies']
    paths = [mod_path + directory for directory in flag_checking_directories]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for flag, start_line in field_contents_gen(contents, 'has_global_flag'):
                if flag not in global_flags_checked:
                    global_flags_checked += [Flag(flag, start_line, filename)]

    global_flags_set_names = set()
    for flag in global_flags_set:
        global_flags_set_names.add(flag.name)
    global_flags_checked_names = set()
    for flag in global_flags_checked:
        global_flags_checked_names.add(flag.name)

    bugs = []
    for flag in global_flags_set:
        if flag.name not in global_flags_checked_names:
            bugs += [Bug('Flag is set but never checked', flag.start_line, flag.filename)]
    for flag in global_flags_modified:
        if flag.name not in global_flags_set_names:
            bugs += [Bug('Flag is modified but never set', flag.start_line, flag.filename)]
    for flag in global_flags_checked:
        if flag.name not in global_flags_set_names:
            bugs += [Bug('Flag is checked but never set', flag.start_line, flag.filename)]
    for flag in global_flags_cleared:
        if flag.name not in global_flags_set_names:
            bugs += [Bug('Flag is cleared but never set', flag.start_line, flag.filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
