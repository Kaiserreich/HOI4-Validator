# By Antoni Baum (Yard1)
# This script parses all events in events folder and returns a dictionary of PDSEvent objects. The key is the event ID.

# http://pyparsing.wikispaces.com/HowToUsePyparsing

from pyparsing import *
import os
import time
from PDSObject import *
from os import listdir
from openFile import open_file

def parse_PDS_script(string): 
    allowed_chars = srange(r"[':a-zA-Z0-9._-]")
    EQUAL = Literal("=").suppress()
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
    pds_member << Group(pds_name("pds_command") + pds_numerical_or_value)
    pds_members << OneOrMore(pds_member)
    pds_list_members << (pds_members | ZeroOrMore(pds_value))

    pds_members.ignore(pythonStyleComment)

    string = pds_members.parseString(string, True)
    return(string)

def get_triggered_text(triggered_text):
    triggered_text = triggered_text[1]
    if isinstance(triggered_text, str):
        return triggered_text
    return next(item[1] for item in triggered_text if len(item) == 2 and item[0] == "text")

def get_true_false_from_yes_no(string):
    return True if string.lower() == "yes" else False

def parse_event_file(event_file):
    namespaces = set()

    print("Reading file %s" % event_file)
    event_file = open_file(event_file).read()

    if not event_file.strip():
        return

    parsed_event_file = parse_PDS_script(event_file)
    for item in [x[1] for x in parsed_event_file if (len(x) == 2 and x[0].lower() == "add_namespace")]:
        namespaces.add(item)

    text_events = [x for x in parsed_event_file if (x and x[0].lower() == "country_event")]
    events = dict()
    for event in text_events:
        if not event:
            continue
        event_type = event[0]
        event = event[1]
        '''
        print("id = \t" + str(next(item[1] for item in event if len(item) == 2 and item[0].lower() == "id")))
        print("title = \t" + str([get_triggered_text(item) for item in event if len(item) == 2 and item[0].lower() == "title"]))
        print("picture = \t" + str(next((item[1] for item in event if len(item) == 2 and item[0].lower() == "picture"), None)))
        print("is_triggered_only = \t" + str(next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "is_triggered_only"), False)))
        print("fire_only_once = \t" + str(next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "fire_only_once"), False)))
        print("hidden = \t" + str(next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "hidden"), False)))
        print("mean_time_to_happen = \t" + str(next((item[1] for item in event if len(item) == 2 and item[0] == "mean_time_to_happen"), None)))
        print("trigger = \t" + str(next((item[1] for item in event if len(item) == 2 and item[0] == "trigger"), None)))
        print("immediate = \t" + str(next((item[1] for item in event if len(item) == 2 and item[0] == "immediate"), None)))
        print("options = \t" + str([item[1] for item in event if len(item) == 2 and item[0] == "option"]))
        '''
        event = PDSEvent(
            event_id=next(item[1] for item in event if len(item) == 2 and item[0] == "id"),
            event_type=event_type,
            title=[get_triggered_text(item) for item in event if len(item) == 2 and item[0] == "title"],
            desc=[get_triggered_text(item) for item in event if len(item) == 2 and item[0] == "desc"],
            picture=next((item[1] for item in event if len(item) == 2 and item[0].lower() == "picture"), None),
            is_triggered_only=next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "is_triggered_only"), False),
            fire_only_once=next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "fire_only_once"), False),
            hidden=next((get_true_false_from_yes_no(item[1]) for item in event if len(item) == 2 and item[0] == "hidden"), False),
            mean_time_to_happen=next((item[1] for item in event if len(item) == 2 and item[0] == "mean_time_to_happen"), None),
            trigger=next((item[1] for item in event if len(item) == 2 and item[0] == "trigger"), None),
            immediate=next((item[1] for item in event if len(item) == 2 and item[0] == "immediate"), None),
            options=[item[1] for item in event if len(item) == 2 and item[0] == "option"]
        )
        if not event.namespace in namespaces:
            raise ValueError('Event %s namespace %s is not in file\'s namespaces.' % (event.event_id, event.namespace))
        events[event.event_id] = event
    print(events)