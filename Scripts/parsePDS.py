# By Antoni Baum (Yard1)
# This script parses all events in events folder and returns a dictionary of PDSEvent objects. The key is the event ID.

# http://pyparsing.wikispaces.com/HowToUsePyparsing

from pyparsing import *
import os
import time
from PDSObject import *
from os import listdir
from openFile import open_file
from logging import log

def make_string_lowercase(s,l,t):
    return t[0].lower()

def parse_PDS_script(string): 
    allowed_chars = srange(r"[':a-zA-Z0-9._-]")
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
    pds_numerical_or_value = ((OPERATOR("pds_operator") + (pds_numerical("pds_numerical") ^ pds_date("pds_date"))) ^ (EQUAL + pds_object))
    pds_member << Group(pds_name("pds_command").setParseAction(make_string_lowercase) + pds_numerical_or_value)
    pds_members << OneOrMore(pds_member)
    pds_list_members << (pds_members | ZeroOrMore(pds_value))

    pds_members.ignore(pythonStyleComment)
    pds_members.enablePackrat()

    string = pds_members.parseString(string, True)
    return(string)

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
    return next((item[2] for item in collection if len(item) == length and item[0] == command), default),

def get_contents_of_multiple_commands(command, collection, default, length=3):
    lst = [item[2] for item in collection if len(item) == length and item[0] == command]
    return lst if lst else default

def parse_localisation(loc_file, loc_dict):
    log("Reading file %s" % loc_file)
    loc_file = open_file(loc_file).read()

    if not loc_file.strip():
        return

    parsed_loc_file = parse_PDS_localisation(loc_file)
    for item in [x for x in parsed_loc_file]:
        loc_dict[item[0]] = item[1]

def parse_event_file(event_file, events_dict):
    namespaces = set()

    log("Reading file %s" % event_file)
    event_file = open_file(event_file).read()

    if not event_file.strip():
        return

    parsed_event_file = parse_PDS_script(event_file)
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
    log(events_dict)

def parse_scripted_effect_file(scripted_effect_file, scripted_effects_dict):

    log("Reading file %s" % scripted_effect_file)
    scripted_effect_file = open_file(scripted_effect_file).read()

    if not scripted_effect_file.strip():
        return

    parsed_scripted_effect_file = parse_PDS_script(scripted_effect_file)
    for item in [x for x in parsed_scripted_effect_file]:
        scripted_effect = PDSScriptedEffect(item[0], item[2])
        scripted_effects_dict[item[0]] = scripted_effect

def parse_scripted_trigger_file(scripted_trigger_file, scripted_triggers_dict):

    log("Reading file %s" % scripted_trigger_file)
    scripted_trigger_file = open_file(scripted_trigger_file).read()

    if not scripted_trigger_file.strip():
        return

    parsed_scripted_trigger_file = parse_PDS_script(scripted_trigger_file)
    for item in [x for x in parsed_scripted_trigger_file]:
        scripted_trigger = PDSScriptedTrigger(item[0], item[2])
        scripted_triggers_dict[item[0]] = scripted_trigger

def parse_focus_file(focus_file, focuses_dict, focus_tree_dict):
    
    log("Reading file %s" % focus_file)
    focus_file = open_file(focus_file).read()

    if not focus_file.strip():
        return

    focus_contents_file = parse_PDS_script(focus_file)
    #log(focus_contents_file)

    for item in focus_contents_file:
        #log(item)
        if item[0] == 'focus_tree':
            focus_tree_id = next(item_2[2] for item_2 in item[2] if len(item_2) == 3 and item_2[0] == "id")
            focus_tree = PDSFocusTree(
                focus_tree_id=focus_tree_id,
                country=get_contents_of_command("country", item[2], None),
                default=get_bool_from_yes_no_str(get_contents_of_command("default", item[2], False)),
                continuous_focus_position=get_contents_of_command("continuous_focus_position", item[2], None)
            )
            focus_tree_dict[focus_tree_id] = focus_tree
            for item in [x for x in item[2] if (x and x[0] == "focus")]:
                focus = create_focus(item, focus_tree_id)
                focuses_dict[focus.focus_id] = focus
                focus_tree.focuses[focus.focus_id] = focus
                log(focus)
            for item in [x for x in item[2] if (x and x[0] == "shared_focus")]:
                focus_tree.shared_focuses.add(item[2])
        elif item[0] == 'focus' or item[0] == 'shared_focus':
            try:
                focus = create_focus(item[0], None)
                focuses_dict[focus.focus_id] = focus
            except ValueError:
                #handle somehow
                pass

def create_focus(focus_contents, focus_tree):
    is_shared = focus_contents[0] == 'shared_focus'
    if is_shared and not focus_tree:
        raise ValueError('focus %s is not shared and outside a focus tree' % next(item[2] for item in focus_contents if len(item) == 3 and item[0] == "id"))
    focus_contents = focus_contents[2]
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
        completion_reward=get_contents_of_command("completion_reward", focus_contents, None),
        completion_tooltip=get_contents_of_command("completion_tooltip", focus_contents, None),
        cancel_if_invalid=get_bool_from_yes_no_str(get_contents_of_command("cancel_if_invalid", focus_contents, False)),
        continue_if_invalid=get_bool_from_yes_no_str(get_contents_of_command("continue_if_invalid", focus_contents, False)),
        available_if_capitulated=get_bool_from_yes_no_str(get_contents_of_command("available_if_capitulated", focus_contents, False)),
    )
    return focus

def parse_idea_file(idea_file, ideas_dict, idea_slots_dict):
    
    log("Reading file %s" % idea_file)
    idea_file = open_file(idea_file).read()

    if not idea_file.strip():
        return

    parsed_idea_file = parse_PDS_script(idea_file)

    for item in parsed_idea_file:
        if item[0] == 'ideas':
            for item_2 in item[2]:
                slot = item_2[0]
                for item_3 in item_2[2]:
                    idea_id = item_3[0]
                    idea = create_idea(idea_id, slot, item_3[2])
                    ideas_dict[idea_id] = idea
                    idea_slots_dict[slot].append(idea)


def create_idea(idea_id, slot, idea_contents):
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