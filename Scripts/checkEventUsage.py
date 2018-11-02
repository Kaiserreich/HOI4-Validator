import collections

from stringAndFileFromPath import files_as_strings_from_path_gen
from timedFunction import timed
from usefulNamedTuples import Bug
from scopeGen import scope_gen
from checkDuplicateIds import find_contents_of_field

Event = collections.namedtuple('Event', 'id start_line filename')
import os
@timed
def check_event_usage(mod_path, output_file):

    non_mtth_events = []

    event_ids = []
    called_ids = []
    called_events = []
    events_directory = '/events/'
    path = os.path.join(mod_path,"events")
    for contents, filename in files_as_strings_from_path_gen(path):
        for event, start_line in scope_gen(contents, ['news_event', 'country_event']):
            event_id = find_contents_of_field(event, 'id')
            if event_id:
                event_ids += [event_id]
            if 'mean_time_to_happen' not in event:
                non_mtth_events += [Event(event_id, start_line, filename)]
            for called_event, called_event_start_line in scope_gen(event, ['news_event', 'country_event']):
                called_event_id = find_contents_of_field(called_event, 'id')
                if called_event_id:
                    called_ids += [called_event_id]
                    called_events += [Event(called_event_id, called_event_start_line+start_line-1, events_directory+filename)]

    directories_that_can_call_events = [os.path.join('common', 'national_focus'),
                                        os.path.join('common', 'on_actions'), 'history',
                                        os.path.join('common', 'decisions'),
                                        ]
    for subdir in directories_that_can_call_events:
        path = os.path.join(mod_path, subdir)
        for contents, filename in files_as_strings_from_path_gen(path):
            for event, start_line in scope_gen(contents, ['news_event', 'country_event']):
                called_event_id = find_contents_of_field(event, 'id')
                if called_event_id:
                    called_ids += [called_event_id]
                    called_events += [Event(find_contents_of_field(event, 'id'), start_line, 'common/'+subdir + filename)]

    bugs = []
    called_ids_set = set(called_ids)
    for event in non_mtth_events:
        if event.id not in called_ids_set:
            bugs += [Bug('Non-MTTH event is not called', event.start_line, event.filename)]

    event_ids_set = set(event_ids)
    for event in called_events:
        if event.id not in event_ids_set:
            bugs += [Bug('Event is called but not defined', event.start_line, event.filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
