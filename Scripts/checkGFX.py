from os import listdir
from os import path
from codecs import open
import re




def check_for_missing_gfx(file_path, output_file):
    print("Just checking")
    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess

    interface_path = file_path + "\\interface"

    tree_path = file_path + "\\common\\national_focus"
    tree_gfx_path = file_path + "\\gfx\\interface\\goals"
    decisions_path = file_path + "\\common\\decisions"
    scripted_triggers_path = file_path + "\\common\\scripted_effects"

    event_path  = file_path + "\\events"
    event_gfx_path = file_path + "\\gfx\\event_pictures"

    ideas_gfx_path = file_path + "\\gfx\\interface\\ideas"
    ideas_gfx_path = file_path + "\\common\\ideas" #also for ministers

    ministers_gfx_path = file_path + "\\gfx\\interface\\ministers"

    tech_gfx_path = file_path + "\\gfx\\interface\\technologies"

    leaders_gfx_path = file_path + "\\gfx\\leaders"
    country_history_path = file_path + "\\history\\countries"

    flags_gfx_path = file_path + "\\gfx\\flags"

    tag = [None] * 600
    fill_tag_array(file_path, tag, True )
    check_flags(tag, flags_gfx_path)

    #Ill also need common\scripted_effects for cosmetic tags
    #fucking flags and their cosmetic tags
    #test


def fill_tag_array(internal_path, tags, cosmetics):

    event_path = internal_path + "\\events"
    tree_path = internal_path + "\\common\\national_focus"
    decisions_path = internal_path + "\\common\\decisions"
    scripted_triggers_path = internal_path + "\\common\\scripted_effects"

    cosmetic_tag_dirs = [event_path, decisions_path, tree_path, scripted_triggers_path]

    #Find Normal Tags
    tags_path = internal_path + "\\common\\country_tags\\00_countries.txt"
    counter = 0
    file = open(tags_path, 'r', 'ansi')
    print("Reading: " + file.name)
    lines = file.readlines()
    for string in lines:
        temp_string = string[:3]
        if '#' not in temp_string and '\r\n' != string:
            tags.append(string[:3])
            #print("Found TAG: " + tags[counter])
            counter += 1
    file.close()

    #Find Cosmetic Tags
    if cosmetics is True:
        for dirs in cosmetic_tag_dirs:
            for filename in listdir(dirs):
                if 'categories' in filename:
                    break
                file = open(dirs + "\\" + filename, 'r', 'utf-8')
                lines = file.readlines()
                for string in lines:
                    if 'set_cosmetic_tag' in string and '#' not in string and '{' not in string:
                        temp_string = string.split(' ')[2][:-2]
                        if finddup(tags, temp_string) is False:
                            tags.append(temp_string)
                            #print("Found TAG: " + cosmetic_tags[counter])
                            counter += 1
    print(counter)


def finddup(array, string):

    try:
        array.index(string)
        return True
    except ValueError:
        return False

def check_flags(tag_array, flag_path):
    print("")
