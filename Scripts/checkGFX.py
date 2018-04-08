from os import listdir
from os import path
from codecs import open
import re

tags = [None] * 300
cosmetic_tags = [None] * 300


def check_for_missing_gfx(file_path, output_file):
    print("Just checking")
    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess

    interface_path = file_path + "\\interface"
    tags_path = file_path + "\\common\\country_tags"

    tree_path = file_path + "\\common\\national_focus"
    tree_gfx_path = file_path + "\\gfx\\interface\\goals"
    decisions_path = file_path + "\\common\\decisions"
    scripted_triggers_path = file_path = "\\common\\scripted_effects"

    event_path  = file_path + "\\events"
    event_gfx_path = file_path + "\\gfx\\event_pictures"

    ideas_gfx_path = file_path + "\\gfx\\interface\\ideas"
    ideas_gfx_path = file_path + "\\common\\ideas" #also for ministers

    ministers_gfx_path = file_path + "\\gfx\\interface\\ministers"

    tech_gfx_path = file_path + "\\gfx\\interface\\technologies"

    leaders_gfx_path = file_path + "\\gfx\\leaders"
    country_history_path = file_path + "\\history\\countries"

    flags_gfx_path = file_path + "\\gfx\\flags"

    cosmetic_tag_dirs = [event_path, decisions_path, tree_path, scripted_triggers_path]
    fill_tags(tags_path)

    #Ill also need common\scripted_effects for cosmetic tags
    #fucking flags and their cosmetic tags
    #test


def fill_tags(internal_path):

    #Find Normal Tags
    counter = 0
    file = open(internal_path + "\\00_countries.txt", 'r', 'utf-8-sig')
    print("Reading: " + file.name)
    lines = file.readlines()
    for string in lines:
        temp_string = string[:3]
        if '#' not in temp_string and '\r\n' != string:
            tags[counter] = string[:3]
            print("Found TAG: " + tags[counter])
            counter += 1

    #Find Cosmetic Tags
    counter = 0
