import collections

from timedFunction import timed
from stringAndFileFromPath import files_as_strings_from_path_gen
from fieldContentsGen import field_contents_gen
from checkEvents import Bug


IdeaUse = collections.namedtuple('IdeaUse', 'name line_number filename')


@timed
def check_idea_usage(mod_path, output_file):
    ideas_added = set()
    ideas_checked = []
    ideas_removed = []

    idea_add_directories = ['//events', '//common//decisions', '//common//scripted_effects',
                            '//common//national_focuses', '//history//countries', '//common//on_actions']
    paths = [mod_path + directory for directory in idea_add_directories]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for idea, line in field_contents_gen(contents, 'add_ideas'):
                ideas_added.add(idea)

    idea_using_directories = ['//events', '//common//decisions', '//common//scripted_triggers',
                                 '//common//scripted localisation', '//common//national_focuses',
                                 '//common//on_actions', '//common//ai_peace', '//common//ai_strategy',
                                 '//common//ai_strategy_plans', '//common//autonomous_states',
                                 '//common//ideas',
                                 '//common//technologies']
    paths = [mod_path + directory for directory in idea_using_directories]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for idea, line in field_contents_gen(contents, 'remove_ideas'):
                ideas_removed += [IdeaUse(idea, line, filename)]
            for idea, line in field_contents_gen(contents, 'has_idea'):
                ideas_checked += [IdeaUse(idea, line, filename)]

    bugs = []
    for idea in ideas_checked:
        if idea.name not in ideas_added:
            bugs += [Bug('Idea is checked but never added', idea.line_number, idea.filename)]
    for idea in ideas_removed:
        if idea.name not in ideas_added:
            bugs += [Bug('Idea is removed but never added', idea.line_number, idea.filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
