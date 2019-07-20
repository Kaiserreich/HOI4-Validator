import collections

from timedFunction import timed
from scopeGen import scope_gen
from stringAndFileFromPath import files_as_strings_from_path_gen
from usefulNamedTuples import Bug
from fieldContentsGen import field_contents_gen
import os
Flag = collections.namedtuple('Flag', 'name start_line filename')


@timed
def check_flag_usage(mod_path, output_file):
    global_flags_set = []
    global_flags_modified = []
    global_flags_checked = []
    global_flags_cleared = []
    country_flags_set = []
    country_flags_modified = []
    country_flags_checked = []
    country_flags_cleared = []
    state_flags_set = []
    state_flags_modified = []
    state_flags_checked = []
    state_flags_cleared = []
    commonpath = os.path.join(mod_path, 'common')
    paths = [os.path.join(mod_path, 'events'), os.path.join(commonpath,'decisions'), os.path.join(commonpath,'scripted_effects'),
                            os.path.join(commonpath,'national_focuses'), os.path.join(mod_path, 'history','countries'), os.path.join(commonpath,'on_actions')]
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

            for flag, start_line in field_contents_gen(contents, 'set_country_flag'):
                if flag not in country_flags_set:
                    country_flags_set += [Flag(flag, start_line, filename)]
            for modify_flag, start_line in scope_gen(contents, ['modify_country_flag']):
                flag, line_offset = next(field_contents_gen(modify_flag, 'flag'))
                if flag not in country_flags_modified:
                    country_flags_modified += [Flag(flag, start_line+line_offset-1, filename)]
            for flag, start_line in field_contents_gen(contents, 'clr_country_flag'):
                if flag not in country_flags_cleared:
                    country_flags_cleared += [Flag(flag, start_line, filename)]

            for flag, start_line in field_contents_gen(contents, 'set_state_flag'):
                if flag not in state_flags_set:
                    state_flags_set += [Flag(flag, start_line, filename)]
            for modify_flag, start_line in scope_gen(contents, ['modify_state_flag']):
                flag, line_offset = next(field_contents_gen(modify_flag, 'flag'))
                if flag not in state_flags_modified:
                    state_flags_modified += [Flag(flag, start_line+line_offset-1, filename)]
            for flag, start_line in field_contents_gen(contents, 'clr_state_flag'):
                if flag not in state_flags_cleared:
                    state_flags_cleared += [Flag(flag, start_line, filename)]

    paths = [os.path.join(mod_path, 'events'),  os.path.join(commonpath,'decisions'),  os.path.join(commonpath,'scripted_triggers'),
            os.path.join(commonpath,'scripted localisation'),  os.path.join(commonpath,'national_focuses'),
            os.path.join(commonpath,'on_actions'),  os.path.join(commonpath,'ai_peace'),  os.path.join(commonpath,'ai_strategy'),
            os.path.join(commonpath,'ai_strategy_plans'),  os.path.join(commonpath,'autonomous_states'),  os.path.join(commonpath,'ideas'),
            os.path.join(commonpath, 'technologies')]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for flag, start_line in field_contents_gen(contents, 'has_global_flag'):
                if flag not in global_flags_checked:
                    global_flags_checked += [Flag(flag, start_line, filename)]
            for flag, start_line in field_contents_gen(contents, 'has_country_flag'):
                if flag not in country_flags_checked:
                    country_flags_checked += [Flag(flag, start_line, filename)]
            if filename != "_Ministers_ideas.txt":
                for flag, start_line in field_contents_gen(contents, 'has_state_flag'):
                    if flag not in state_flags_checked:
                        state_flags_checked += [Flag(flag, start_line, filename)]

    global_flags_set_names = set()
    for flag in global_flags_set:
        global_flags_set_names.add(flag.name)
    global_flags_checked_names = set()
    for flag in global_flags_checked:
        global_flags_checked_names.add(flag.name)

    country_flags_set_names = set()
    for flag in country_flags_set:
        country_flags_set_names.add(flag.name)
    country_flags_checked_names = set()
    for flag in country_flags_checked:
        country_flags_checked_names.add(flag.name)

    state_flags_set_names = set()
    for flag in state_flags_set:
        state_flags_set_names.add(flag.name)
    state_flags_checked_names = set()
    for flag in state_flags_checked:
        state_flags_checked_names.add(flag.name)

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

    for flag in country_flags_set:
        if flag.name not in country_flags_checked_names:
            bugs += [Bug('Flag is set but never checked', flag.start_line, flag.filename)]
    for flag in country_flags_modified:
        if flag.name not in country_flags_set_names:
            bugs += [Bug('Flag is modified but never set', flag.start_line, flag.filename)]
    for flag in country_flags_checked:
        if flag.name not in country_flags_set_names:
            bugs += [Bug('Flag is checked but never set', flag.start_line, flag.filename)]
    for flag in country_flags_cleared:
        if flag.name not in country_flags_set_names:
            bugs += [Bug('Flag is cleared but never set', flag.start_line, flag.filename)]

    for flag in state_flags_set:
        if flag.name not in state_flags_checked_names:
            bugs += [Bug('Flag is set but never checked', flag.start_line, flag.filename)]
    for flag in state_flags_modified:
        if flag.name not in state_flags_set_names:
            bugs += [Bug('Flag is modified but never set', flag.start_line, flag.filename)]
    for flag in state_flags_checked:
        if flag.name not in state_flags_set_names:
            bugs += [Bug('Flag is checked but never set', flag.start_line, flag.filename)]
    for flag in state_flags_cleared:
        if flag.name not in state_flags_set_names:
            bugs += [Bug('Flag is cleared but never set', flag.start_line, flag.filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
