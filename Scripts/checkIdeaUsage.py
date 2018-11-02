import collections

from timedFunction import timed
from stringAndFileFromPath import files_as_strings_from_path_gen
from fieldContentsGen import field_contents_gen
from usefulNamedTuples import Bug
import os

IdeaUse = collections.namedtuple('IdeaUse', 'name line_number filename')


@timed
def check_idea_usage(mod_path, output_file):
    ideas_added = set()
    ideas_checked = []
    ideas_removed = []

    paths = [os.path.join(mod_path, 'events'), os.path.join(mod_path, 'common','decisions'), os.path.join(mod_path, 'common','scripted_effects'),
                            os.path.join(mod_path, 'common','national_focuses'), os.path.join(mod_path, 'history','countries'), os.path.join(mod_path, 'common','on_actions')]
    for path in paths:
        for contents, filename in files_as_strings_from_path_gen(path):
            for idea, line in field_contents_gen(contents, 'add_ideas'):
                ideas_added.add(idea)

    idea_using_directories = [os.path.join(mod_path, 'events'), os.path.join(mod_path, 'common','decisions'), os.path.join(mod_path, 'common','scripted_triggers'),
                            os.path.join(mod_path, 'common','national_focuses'),
                                 os.path.join(mod_path, 'common','scripted localisation'), os.path.join(mod_path, 'common','national_focuses'),
                                 os.path.join(mod_path, 'common','on_actions'), os.path.join(mod_path, 'common','ai_peace'), os.path.join(mod_path, 'common','ai_strategy'),
                                 os.path.join(mod_path, 'common','ai_strategy_plans'), os.path.join(mod_path, 'common','autonomous_states'),
                                 os.path.join(mod_path, 'common','ideas'),
                                 os.path.join(mod_path, 'common','technologies')]
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
