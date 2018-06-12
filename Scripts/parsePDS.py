# By Antoni Baum (Yard1)
# This script parses all events in events folder and returns a dictionary of PDSEvent objects. The key is the event ID.

# http://pyparsing.wikispaces.com/HowToUsePyparsing

from pyparsing import *
import os
import time
from PDSObject import *
from os import listdir
from openFile import open_file

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

def get_true_false_from_yes_no(string):
    return True if string == "yes" else False

def parse_localisation(loc_file, loc_dict):
    print("Reading file %s" % loc_file)
    loc_file = open_file(loc_file).read()

    if not loc_file.strip():
        return

    parsed_loc_file = parse_PDS_localisation(loc_file)
    for item in [x for x in parsed_loc_file]:
        loc_dict[item[0]] = item[1]

def parse_event_file(event_file, events_dict):
    namespaces = set()

    print("Reading file %s" % event_file)
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
            event_id=next(item[2] for item in event if len(item) == 3 and item[0] == "id"),
            event_type=event_type,
            title=[get_triggered_text(item) for item in event if len(item) == 3 and item[0] == "title"],
            desc=[get_triggered_text(item) for item in event if len(item) == 3 and item[0] == "desc"],
            picture=next((item[2] for item in event if len(item) == 3 and item[0] == "picture"), None),
            is_triggered_only=next((get_true_false_from_yes_no(item[2]) for item in event if len(item) == 3 and item[0] == "is_triggered_only"), False),
            fire_only_once=next((get_true_false_from_yes_no(item[2]) for item in event if len(item) == 3 and item[0] == "fire_only_once"), False),
            hidden=next((get_true_false_from_yes_no(item[2]) for item in event if len(item) == 3 and item[0] == "hidden"), False),
            mean_time_to_happen=next((item[2] for item in event if len(item) == 3 and item[0] == "mean_time_to_happen"), None),
            trigger=next((item[2] for item in event if len(item) == 3 and item[0] == "trigger"), None),
            immediate=next((item[2] for item in event if len(item) == 3 and item[0] == "immediate"), None),
            options=[item[2] for item in event if len(item) == 3 and item[0] == "option"]
        )
        if not event.namespace in namespaces:
            raise ValueError('Event %s namespace %s is not in file\'s namespaces.' % (event.event_id, event.namespace))
        events_dict[event.event_id] = event
    print(events_dict)

def parse_scripted_effect_file(scripted_effect_file, scripted_effects_dict):

    print("Reading file %s" % scripted_effect_file)
    scripted_effect_file = open_file(scripted_effect_file).read()

    if not scripted_effect_file.strip():
        return

    parsed_scripted_effect_file = parse_PDS_script(scripted_effect_file)
    for item in [x for x in parsed_scripted_effect_file]:
        scripted_effect = PDSScriptedEffect(item[0], item[2])
        scripted_effects_dict[item[0]] = scripted_effect

def parse_scripted_trigger_file(scripted_trigger_file, scripted_triggers_dict):

    print("Reading file %s" % scripted_trigger_file)
    scripted_trigger_file = open_file(scripted_trigger_file).read()

    if not scripted_trigger_file.strip():
        return

    parsed_scripted_trigger_file = parse_PDS_script(scripted_trigger_file)
    for item in [x for x in parsed_scripted_trigger_file]:
        scripted_trigger = PDSScriptedTrigger(item[0], item[2])
        scripted_triggers_dict[item[0]] = scripted_trigger

def parse_focus_file(focus_file, focuses_dict, focus_tree_dict):
    
    print("Reading file %s" % focus_file)
    focus_file = open_file(focus_file).read()

    if not focus_file.strip():
        return

    parsed_focus_file = parse_PDS_script(focus_file)
    #print(parsed_focus_file)

    for item in parsed_focus_file:
        #print(item)
        if item[0] == 'focus_tree':
            focus_tree_id = next(item_2[2] for item_2 in item[2] if len(item_2) == 3 and item_2[0] == "id")
            focus_tree = PDSFocusTree(
                focus_tree_id=focus_tree_id,
                country=next(item_2[2] for item_2 in item[2] if len(item_2) == 3 and item_2[0] == "country"),
                default=next((get_true_false_from_yes_no(item_2[2]) for item_2 in item[2] if len(item_2) == 3 and item_2[0] == "default"), False),
                continuous_focus_position=next((item_2[2] for item_2 in item[2] if len(item_2) == 3 and item_2[0] == "continuous_focus_position"), None)
            )
            focus_tree_dict[focus_tree_id] = focus_tree
            for item in [x for x in item[2] if (x and x[0] == "focus")]:
                focus = create_focus(item, focus_tree_id)
                focuses_dict[focus.focus_id] = focus
                focus_tree.focuses[focus.focus_id] = focus
                print(focus)
            for item in [x for x in item[2] if (x and x[0] == "shared_focus")]:
                focus_tree.shared_focuses.add(item[2])
        elif item[0] == 'focus' or item[0] == 'shared_focus':
            try:
                focus = create_focus(item[0], None)
                focuses_dict[focus.focus_id] = focus
            except ValueError:
                #handle somehow
                pass

def create_focus(parsed_focus, focus_tree):
    is_shared = parsed_focus[0] == 'shared_focus'
    if is_shared and not focus_tree:
        raise ValueError('focus %s is not shared and outside a focus tree' % next(item[2] for item in parsed_focus if len(item) == 3 and item[0] == "id"))
    parsed_focus = parsed_focus[2]
    focus = PDSFocus(
        focus_id=next(item[2] for item in parsed_focus if len(item) == 3 and item[0] == "id"),
        is_shared=is_shared,
        focus_tree=focus_tree,
        cost=next(item[2] for item in parsed_focus if len(item) == 3 and item[0] == "cost"),
        icon=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "icon"), None),
        prerequisite=[item[2] for item in parsed_focus if len(item) == 3 and item[0] == "prerequisite"],
        mutually_exclusive=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "mutually_exclusive"), None),
        available=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "available"), None),
        bypass=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "bypass"), None),
        allow_branch=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "allow_branch"), None),
        x=next(item[2] for item in parsed_focus if len(item) == 3 and item[0] == "x"),
        y=next(item[2] for item in parsed_focus if len(item) == 3 and item[0] == "y"),
        relative_position_id=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "relative_position_id"), None),
        offset=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "offset"), None),
        ai_will_do=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "ai_will_do"), None),
        completion_reward=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "completion_reward"), None),
        completion_tooltip=next((item[2] for item in parsed_focus if len(item) == 3 and item[0] == "completion_tooltip"), None),
        cancel_if_invalid=next((get_true_false_from_yes_no(item[2]) for item in parsed_focus if len(item) == 3 and item[0] == "cancel_if_invalid"), False),
        continue_if_invalid=next((get_true_false_from_yes_no(item[2]) for item in parsed_focus if len(item) == 3 and item[0] == "continue_if_invalid"), False),
        available_if_capitulated=next((get_true_false_from_yes_no(item[2]) for item in parsed_focus if len(item) == 3 and item[0] == "available_if_capitulated"), False),
    )
    return focus

parse_focus_file("national_focus/KR_Brazil.txt", None, None)