import enum
import re

class PDSEvent:
    def __init__(self, event_id, event_type, title, desc, picture, is_triggered_only, fire_only_once, hidden, mean_time_to_happen, trigger, immediate, options):
        self.event_id = event_id
        self.event_type = event_type
        self.namespace = re.search(".*(?=\.)", event_id).group()
        self.title = title
        self.desc = desc
        self.picture = picture
        self.is_triggered_only = is_triggered_only
        self.fire_only_once = fire_only_once
        self.hidden = hidden
        self.mean_time_to_happen = mean_time_to_happen
        if mean_time_to_happen:
            if is_triggered_only:
                raise ValueError('Has both is_triggered_only and mean_time_to_happen')
            if len(mean_time_to_happen) != 1:
                raise ValueError('Too many mean_time_to_happen arguments - %s, has to be 1' % str(len(mean_time_to_happen)))
        self.trigger = trigger
        self.immediate = immediate
        self.options = options
        self.references = []
'''
class PDSScriptedEvent:
    #TODO

class PDSScriptedTrigger:
    #TODO

class PDSFocus:
    #TODO

class PDSFocusTree:
    #TODO

class PDSDecision:
    #TODO

class PDSOOB:
    #TODO

class PDSCountryHistory:
    #TODO

class PDSStateHistory:
    #TODO

class PDSIdea:
    #TODO

class PDSGFX:
    #TODO

class PDSLocalisation:
    #TODO

class PDSUnitLeader:
    #TODO
'''