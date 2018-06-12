import enum
import re

class PDSEvent:
    def __init__(self, event_id, event_type, title, desc, picture, is_triggered_only, fire_only_once, hidden, mean_time_to_happen, trigger, immediate, options):
        self.event_id = event_id
        self.event_type = event_type
        self.namespace = re.search(r".*(?=\.)", event_id).group()
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

class PDSScriptedEffect:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

class PDSScriptedTrigger:
    def __init__(self, name, trigger):
        self.name = name
        self.trigger = trigger


class PDSFocus:
    def __init__(self, focus_id, is_shared, focus_tree, icon, prerequisite, mutually_exclusive, available, bypass, allow_branch, x, y, relative_position_id, offset, cost, ai_will_do, completion_reward, completion_tooltip, cancel_if_invalid, continue_if_invalid, available_if_capitulated):
        self.focus_id = focus_id
        self.is_shared = is_shared
        self.focus_tree = focus_tree
        self.icon = icon
        self.prerequisite = prerequisite
        if prerequisite:
            for idx, item in enumerate(prerequisite):
                prerequisite[idx] = [x[2] for x in item]
        self.mutually_exclusive = mutually_exclusive
        if mutually_exclusive:
            mutually_exclusive = [x[2] for x in mutually_exclusive]
        self.available = available
        self.bypass = bypass
        self.allow_branch = allow_branch
        self.x = x
        self.real_x = x
        self.y = y
        self.real_y = y
        self.relative_position_id = relative_position_id
        self.offset = offset
        self.ai_will_do = ai_will_do
        self.completion_reward = completion_reward
        self.completion_tooltip = completion_tooltip
        self.cancel_if_invalid = cancel_if_invalid
        self.continue_if_invalid = continue_if_invalid
        self.available_if_capitulated = available_if_capitulated


class PDSFocusTree:
    def __init__(self, focus_tree_id, country, default, continuous_focus_position):
        self.focus_tree_id = focus_tree_id
        self.country = country
        self.default = default
        self.continuous_focus_position = continuous_focus_position
        if continuous_focus_position:
            continuous_focus_position = (next(item[2] for item in continuous_focus_position if len(item) == 3 and item[0] == "x"), next(item[2] for item in continuous_focus_position if len(item) == 3 and item[0] == "y"))
        self.focuses = dict()
        self.shared_focuses = set()
'''
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

class PDSScriptedLocalisation:
    #TODO

class PDSUnitLeader:
    #TODO
'''