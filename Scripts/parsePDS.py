# By Antoni Baum (Yard1)
# This script parses all events in events folder and returns a dictionary of PDSEvent objects. The key is the event ID.

# http://pyparsing.wikispaces.com/HowToUsePyparsing

import psutil
from memory_profiler import profile
from pyparsing import *
ParserElement.enablePackrat()
import os
import sys
import time
from PDSObject import *
from os import listdir
from openFile import open_file
from validator_logging import LOGGER as Logger
from validator_logging import LogLevel
import pathos
import gc
from collections import defaultdict

def make_string_lowercase(s,l,t):
    if not len(t[0]) == 3:
        return t[0].lower()

class PDSParser():
    allowed_chars = srange("[':a-zA-Z0-9._\-@]")
    EQUAL = Literal("=")
    OPERATOR = oneOf("< > =")
    LBRACE = Literal("{").suppress()
    RBRACE = Literal("}").suppress()
    
    pds_name = Word(allowed_chars)
    pds_numerical = Combine(Optional("-") + Word(nums) + Optional("." + Word(nums)))
    pds_date = Combine(Word(nums) + "." + Word(nums) + "." + Word(nums))
    pds_string = dblQuotedString().setParseAction(removeQuotes)
    pds_member = Forward()
    pds_members = Forward()
    pds_list_members = Forward()
    pds_object = Forward()
    pds_value = Forward()
    pds_list = Group(LBRACE + pds_list_members + RBRACE)
    pds_object << (pds_string("pds_quoted_argument") | pds_name("pds_agrument") | pds_list("pds_list"))
    pds_value << (pds_string("pds_quoted_list_item") | pds_name("pds_list_item"))
    pds_numerical_or_value = (OPERATOR("pds_operator") + (pds_numerical("pds_numerical") ^ pds_date("pds_date") ^ pds_object("pds_object")))
    pds_member << Group((pds_name("pds_command").setParseAction(make_string_lowercase) | pds_string("pds_quoted_argument")) + pds_numerical_or_value)
    pds_members << OneOrMore(pds_member)
    pds_list_members << (pds_members | ZeroOrMore(pds_value))

    pds_member.ignore(pythonStyleComment)
    pds_members.ignore(pythonStyleComment)
    #pds_members.setDebug()

    def parse_PDS_script(self, string): 
        if not string.strip():
            return string
        #Logger.log(string[:100])
        string = self.pds_members.parseString(string, True)
        #gc.collect()
        return(string)

PARSER = PDSParser()
PREPARSE_LOCK = pathos.helpers.mp.Lock()
def preparse_PDS_script(string, start, end, lock=PREPARSE_LOCK, use_category=True):
    blocks = defaultdict(list) if use_category else []
    open_braces = 0
    start_idx_set = False
    start_idx = 0
    end_idx_set = False
    end_idx = 0
    is_comment = False
    is_quoted = False #Stop-gap
    if use_category:
        category = ""
        current_category = ""
    string = re.sub(r"#.*\n", "", string).strip()
    string = re.sub(r"\blog\b\s*=\s*\".*?\"", "", string)
    for idx, c in enumerate(string):
        if c == '#':
            is_comment = True

        if is_comment:
            if c == '\n':
                is_comment = False
            continue

        if c == '}':
            open_braces -= 1

        if open_braces == start:
            if use_category:
                if category:
                    current_category = category.strip().split()[-2]
                category = ""
            if not start_idx_set:
                start_idx = idx
                start_idx_set = True
            end_idx_set = False
        
        if c == '{':
            open_braces += 1

        if use_category and open_braces == end:
            category += c

        if open_braces == end:
            if not end_idx_set:
                end_idx = idx
                end_idx_set = True
            if end_idx > start_idx and start_idx_set:
                block = string[start_idx:end_idx]
                block = block.strip()
                if block:
                    lock.acquire()
                    if use_category:
                        blocks[current_category].append(block)
                    else:
                        blocks.append(block)
                    lock.release()
                start_idx_set = False
    return blocks

def parse_PDS_localisation(string):
    allowed_chars = srange(r"['a-zA-Z0-9._-]")
    pds_loc = Word(allowed_chars) + (":" + Word(nums)).suppress() + dblQuotedString()
    pds_loc.setDebug()
    pds_loc.ignore(pythonStyleComment)
    string = pds_loc.parseString(string, True)
    return(string)

def get_triggered_text(triggered_text):
    triggered_text = triggered_text[2]
    if isinstance(triggered_text, str):
        return triggered_text
    return next(item[2] for item in triggered_text if len(item) == 3 and item[0] == "text")

def get_bool_from_yes_no_str(string):
    if isinstance(string, bool):
        return string
    return True if string == "yes" else False

def get_contents_of_command(command, collection, default, length=3):
    return next((item[2] for item in collection if len(item) == length and item[0] == command), default)

def get_contents_of_multiple_commands(command, collection, default, length=3):
    lst = [item[2] for item in collection if len(item) == length and item[0] == command]
    return lst if lst else default

def parse_localisation(loc_file, loc_dict):
    Logger.log("Reading file %s" % loc_file, level=LogLevel.Info)
    loc_file = open_file(loc_file)

    if not loc_file.strip():
        return

    parsed_loc_file = parse_PDS_localisation(loc_file)
    for item in [x for x in parsed_loc_file]:
        loc_dict[item[0]] = item[1]

def parse_event_file(event_file, events_dict):
    namespaces = set()

    Logger.log("Reading file %s" % event_file, level=LogLevel.Info)
    event_file = open_file(event_file)

    if not event_file.strip():
        return

    parsed_event_file = PARSER.parse_PDS_script(event_file)
    for item in [x[2] for x in parsed_event_file if (len(x) == 3 and x[0]== "add_namespace")]:
        namespaces.add(item)

    text_events = [x for x in parsed_event_file if (x and x[0] == "country_event")]
    for event in text_events:
        if not event:
            continue
        event_type = event[0]
        event = event[1]

        event = PDSEvent(
            event_id=get_contents_of_command("id", event, None),
            event_type=event_type,
            title=[get_triggered_text(item) for item in event if len(item) == 3 and item[0] == "title"],
            desc=[get_triggered_text(item) for item in event if len(item) == 3 and item[0] == "desc"],
            picture=get_contents_of_command("picture", event, None),
            is_triggered_only=get_bool_from_yes_no_str(get_contents_of_command("is_triggered_only", event, False)),
            fire_only_once=get_bool_from_yes_no_str(get_contents_of_command("fire_only_once", event, False)),
            hidden=get_bool_from_yes_no_str(get_contents_of_command("hidden", event, False)),
            mean_time_to_happen=get_contents_of_command("mean_time_to_happen", event, None),
            trigger=get_contents_of_command("trigger", event, None),
            immediate=get_contents_of_command("immediate", event, None),
            options=get_contents_of_multiple_commands("option", event, None)
        )
        if not event.namespace in namespaces:
            raise ValueError('Event %s namespace %s is not in file\'s namespaces.' % (event.event_id, event.namespace))
        events_dict[event.event_id] = event
    Logger.log(events_dict, level=LogLevel.Debug)

def parse_scripted_effect_file(scripted_effect_file, scripted_effects_dict):

    Logger.log("Reading file %s" % scripted_effect_file, level=LogLevel.Info)
    scripted_effect_file = open_file(scripted_effect_file)

    if not scripted_effect_file.strip():
        return

    parsed_scripted_effect_file = PARSER.parse_PDS_script(scripted_effect_file)
    for item in [x for x in parsed_scripted_effect_file]:
        scripted_effect = PDSScriptedEffect(item[0], item[2])
        scripted_effects_dict[item[0]] = scripted_effect

def parse_scripted_trigger_file(scripted_trigger_file, scripted_triggers_dict):

    Logger.log("Reading file %s" % scripted_trigger_file, level=LogLevel.Info)
    scripted_trigger_file = open_file(scripted_trigger_file)

    if not scripted_trigger_file.strip():
        return

    parsed_scripted_trigger_file = PARSER.parse_PDS_script(scripted_trigger_file)
    for item in [x for x in parsed_scripted_trigger_file]:
        scripted_trigger = PDSScriptedTrigger(item[0], item[2])
        scripted_triggers_dict[item[0]] = scripted_trigger

def preparse_focus_file(focus_file):
    Logger.log("Reading file %s" % focus_file, level=LogLevel.Info)
    focus_file = open_file(focus_file)

    if not focus_file.strip():
        return
    focuses_in_focus_trees = defaultdict(list)
    preparsed_focuses = preparse_PDS_script(focus_file, 1, 0)
    focus_tree_properties = defaultdict(list)
    if 'focus_tree' in preparsed_focuses:
        for item in preparsed_focuses['focus_tree']:
            focus_tree_id = PARSER.parse_PDS_script(re.search(r"\bid\s*=\s*.*\b", item).group(0))[0][2]
            if focus_tree_id == 'focus':
                Logger.log(focus_tree_id, preparsed_focuses)
            assert focus_tree_id != 'shared_focus'
            shared_focus_ids_temp = set()
            for shared_focus_id in re.findall(r"\bshared_focus\s*=\s*.*\b", item):
                shared_focus_ids_temp.add(PARSER.parse_PDS_script(shared_focus_id)[0][2])
            try:
                default = get_bool_from_yes_no_str(PARSER.parse_PDS_script(re.search(r"\bdefault\s*=\s*.*\b", item).group(0))[0][2])
            except:
                default = False
            focuses_in_focus_trees[focus_tree_id].append(preparse_PDS_script(item, 1, 0))
            country = PARSER.parse_PDS_script(focuses_in_focus_trees[focus_tree_id][0]['country'][0])
            try:
                continuous_focus_position = PARSER.parse_PDS_script(focuses_in_focus_trees[focus_tree_id][0]['continuous_focus_position'])
            except:
                continuous_focus_position = None

            focus_tree_properties[focus_tree_id].append(country)
            focus_tree_properties[focus_tree_id].append(default)
            focus_tree_properties[focus_tree_id].append(continuous_focus_position)
            focus_tree_properties[focus_tree_id].append(shared_focus_ids_temp)

        for key, lst in focuses_in_focus_trees.items():
            for dct in lst:
                if dct:
                    for _, value in dct.items():
                        preparsed_focuses[key].extend(value)
    preparsed_focuses.pop('focus_tree', None)
    #Logger.log(preparsed_focuses)
    return (preparsed_focuses, focus_tree_properties)


def parse_focus(key, value):
    value = PARSER.parse_PDS_script(value)
    #Logger.log(focus_contents_file)
    focuses_dict = dict()
    focuse_trees_dict = defaultdict(list)
    try:
        focus = create_focus(value, key)
        if focus:
            focuses_dict[focus.focus_id] = focus
            focuse_trees_dict[key].append(focus)
    except ValueError:
        #handle somehow
        pass
    return (focuses_dict, focuse_trees_dict)

def create_focus(focus_contents, focus_tree):
    #Logger.log("%s %s" % (get_contents_of_command("id", focus_contents, None), focus_tree))
    if not get_contents_of_command("id", focus_contents, None):
        # handle
        return
    is_shared = focus_tree == 'shared_focus'
    focus = PDSFocus(
        focus_id=get_contents_of_command("id", focus_contents, None),
        is_shared=is_shared,
        focus_tree=focus_tree,
        cost=get_contents_of_command("cost", focus_contents, None),
        icon=get_contents_of_command("icon", focus_contents, None),
        prerequisite=get_contents_of_multiple_commands("prerequisite", focus_contents, None),
        mutually_exclusive=get_contents_of_command("mutually_exclusive", focus_contents, None),
        available=get_contents_of_command("available", focus_contents, None),
        bypass=get_contents_of_command("bypass", focus_contents, None),
        allow_branch=get_contents_of_command("allow_branch", focus_contents, None),
        x=get_contents_of_command("x", focus_contents, -1),
        y=get_contents_of_command("y", focus_contents, -1),
        relative_position_id=get_contents_of_command("relative_position_id", focus_contents, None),
        offset=get_contents_of_command("offset", focus_contents, None),
        ai_will_do=get_contents_of_command("ai_will_do", focus_contents, None),
        select_effect=get_contents_of_command("select_effect", focus_contents, None),
        completion_reward=get_contents_of_command("completion_reward", focus_contents, None),
        completion_tooltip=get_contents_of_command("completion_tooltip", focus_contents, None),
        cancel_if_invalid=get_bool_from_yes_no_str(get_contents_of_command("cancel_if_invalid", focus_contents, False)),
        continue_if_invalid=get_bool_from_yes_no_str(get_contents_of_command("continue_if_invalid", focus_contents, False)),
        available_if_capitulated=get_bool_from_yes_no_str(get_contents_of_command("available_if_capitulated", focus_contents, False)),
    )
    return focus

#@profile
def preparse_idea_file(idea_file):
    Logger.log("Reading file %s" % idea_file, level=LogLevel.Info)
    idea_file = open_file(idea_file)

    if not idea_file.strip():
        return

    return preparse_PDS_script(idea_file, 2, 1)

def parse_idea(key, value):
    slot = key
    ideas = dict()
    idea_slots = defaultdict(list)
    for item in value:
        parsed_idea = PARSER.parse_PDS_script(item)
        for item_2 in parsed_idea:
            if isinstance(item_2[2], ParseResults):
                idea_id = item_2[0]
                idea = create_idea(idea_id, slot, item_2[2])
                ideas[idea_id] = idea
                idea_slots[slot].append(idea)
    return (ideas, idea_slots)

def create_idea(idea_id, slot, idea_contents):
    Logger.log("%s %s" % (idea_id, slot))
    idea = PDSIdea(
        idea_id=idea_id,
        slot=slot,
        picture=get_contents_of_command("picture", idea_contents, idea_id),
        level=get_contents_of_command("level", idea_contents, -1),
        cost=get_contents_of_command("cost", idea_contents, 0), #make sure it's 0
        removal_cost=get_contents_of_command("removal_cost", idea_contents, -1), #make sure it's -1
        allowed=get_contents_of_command("allowed", idea_contents, None),
        allowed_civil_war=get_contents_of_command("allowed_civil_war", idea_contents, None),
        allowed_to_remove=get_contents_of_command("allowed_to_remove", idea_contents, None),
        available=get_contents_of_command("available", idea_contents, None),
        ai_will_do=get_contents_of_command("ai_will_do", idea_contents, None),
        on_add=get_contents_of_command("on_add", idea_contents, None),
        on_remove=get_contents_of_command("on_remove", idea_contents, None),
        do_effect=get_contents_of_command("do_effect", idea_contents, None),
        equipment_bonus=get_contents_of_command("equipment_bonus", idea_contents, None),
        research_bonus=get_contents_of_command("research_bonus", idea_contents, None),
        modifier=get_contents_of_command("modifier", idea_contents, None),
        targeted_modifier=get_contents_of_multiple_commands("targeted_modifier", idea_contents, None),
        rule=get_contents_of_command("rule", idea_contents, None),
        traits=get_contents_of_command("traits", idea_contents, None),
        cancel_if_invalid=get_bool_from_yes_no_str(get_contents_of_command("cancel_if_invalid", idea_contents, False)),
        default=get_bool_from_yes_no_str(get_contents_of_command("default", idea_contents, False)),
    )
    return idea