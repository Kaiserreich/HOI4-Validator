from scopeGen import scope_gen
from stringAndFileFromPath import files_as_strings_from_path_gen
from fieldContentsGen import field_contents_gen
from timedFunction import timed
import os

from usefulNamedTuples import Bug


@timed
def check_events(mod_path, output_file, optionsdict):
    if optionsdict['check_ai_chance_usage'] or optionsdict['check_events_for_graphics'] or optionsdict['check_events_for_titles'] or optionsdict['check_events_for_descriptions'] or optionsdict['check_events_for_options'] or optionsdict['check_load_oob_usage'] or optionsdict['check_for_duplicate_options_loc'] or optionsdict['check_hidden_events']:
        bugs = []
        path = os.path.join(mod_path,"events")
        for contents, filename in files_as_strings_from_path_gen(path):
            for event, start_line in scope_gen(contents, ['news_event', 'country_event']):
                if optionsdict['check_ai_chance_usage']:
                    if 'ai_chance' in event and event.count('option =') == 1:
                        bugs.append(Bug('\"ai_chance\" with only one option in event', start_line, filename))
                if 'hidden = yes' not in event:
                    if optionsdict['check_events_for_graphics']:
                        if 'picture =' not in event:
                            bugs.append(Bug('No picture for event', start_line, filename))
                    if optionsdict['check_events_for_titles']:
                        if 'title =' not in event:
                            bugs.append(Bug('No title for event', start_line, filename))
                    if optionsdict['check_events_for_descriptions']:
                        if 'desc =' not in event:
                            bugs.append(Bug('No description for event', start_line, filename))
                    if optionsdict['check_events_for_options']:
                        if 'option =' not in event:
                            bugs.append(Bug('No options for event', start_line, filename))
                    if optionsdict['check_load_oob_usage']:
                        if 'load_oob' in event and 'custom_effect_tooltip' not in event:
                            bugs.append(Bug('\"load_oob\" is an effect but there is no \"custom_effect_tooltip\" in event', start_line, filename))
                    if optionsdict['check_for_duplicate_options_loc']:
                        option_locs = []
                        for option, option_start_line in scope_gen(event, ['option']):
                            try:
                                loc, loc_line = next(field_contents_gen(option, 'name'))
                                if loc in option_locs:
                                    bugs.append(Bug('Duplicate option localization in event', start_line+option_start_line+1, filename))
                                option_locs.append(loc)
                            except StopIteration:
                                pass
                if optionsdict['check_hidden_events']:
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


