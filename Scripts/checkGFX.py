from os import listdir
from os import walk
from os import path
from codecs import open
import time

def check_for_missing_gfx(file_path, output_file, hoi4_path):
    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess
    t0 = time.time()

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

    check_flags(flags_gfx_path, output_file, file_path)

    check_events(event_path, event_gfx_path,interface_path, file_path, output_file, hoi4_path)

    t0 = time.time()- t0
    print("Time taken for GFX script: " + (t0*1000).__str__() + " ms")


def fill_tag_array(internal_path, cosmetics):
    # 0 = just normal
    # 1 = just cosmetic
    # 2 = both

    tags = []
    event_path = internal_path + "\\events"
    tree_path = internal_path + "\\common\\national_focus"
    decisions_path = internal_path + "\\common\\decisions"
    scripted_triggers_path = internal_path + "\\common\\scripted_effects"

    cosmetic_tag_dirs = [event_path, decisions_path, tree_path, scripted_triggers_path]

    #Find Normal Tags
    tags_path = internal_path + "\\common\\country_tags\\00_countries.txt"
    file = open(tags_path, 'r', 'ansi')
    #print("Reading: " + file.name)
    lines = file.readlines()

    if cosmetics != 1:
        for string in lines:
            temp_string = string[:3]
            if '#' not in temp_string and '\r\n' != string:
                tags.append(string[:3])
                #print("Found TAG: " + tags[counter])

    #Find Cosmetic Tags
    if cosmetics != 0:
        for dirs in cosmetic_tag_dirs:
            for filename in listdir(dirs):
                if 'categories' in filename:
                    continue
                file = open(dirs + "\\" + filename, 'r', 'utf-8')
                lines = file.readlines()
                for string in lines:
                    if 'set_cosmetic_tag' in string and string.strip().startswith('#') is False and '{' not in string:
                        temp_string = string.split(' ')[2][:-2]
                        if finddup(tags, temp_string) is False:
                            tags.append(temp_string)
                            #print("Found TAG: " + temp_string)
    return tags


def finddup(array, string):
    if string in array:
        return True
    else:
        return False


def hasideo(string, idarray):
    for ideos in idarray:
        if ideos in string:
            return True
    return False


def stripideo(string, idarray):
    for ideos in idarray:
        if ideos in string:
            return string[:-len(ideos)-1]


def check_flags( flag_path, output_file, file_path):
    ideos = ["totalist", "syndicalist", "radical_socialist", "social_democrat", "social_liberal", "market_liberal", "social_conservative", "authoritarian_democrat", "paternal_autocrat", "national_populist"]
    flagarr = []

    tag_array = fill_tag_array(file_path, 2)

    for file_name in listdir(flag_path):
        if 'medium' in file_name or 'small' in file_name:
            continue
        temp_string = file_name[:-4]
        if hasideo(temp_string, ideos) is True:
            temp_string = stripideo(temp_string, ideos)
        if finddup(tag_array, temp_string) is False:
            #print("No tag for " + file_name)
            output_file.write("No (cosmetic) tag for " + file_name + "\n")
        if finddup(flagarr, temp_string) is False:
            flagarr.append(temp_string)
            #print(temp_string)
    tag_array = fill_tag_array(file_path, 0)
    for strings in tag_array:
        if finddup(flagarr, strings) is False:
            output_file.write("No flag for " + strings + "\n")
            #print("No flag for " + strings)

def check_events(event_path, event_gfx_path, interface_path, file_path, output_file, hoi4path):

    #Fill Both the Leader pictures and the event pictures
    amountarr = []
    event_picture = []
    leader_picture = []
    for file_name in listdir(event_path):
        line_number = 0
        file = open(event_path + "\\" + file_name, 'r', 'utf-8')
        lines = file.readlines()
        for line in lines:
            line_number += 1
            if "picture" in line and line.strip().startswith('#') is False:
                if '#' in line:
                    line = line.split('#')[0].strip()
                temp_string = line.strip()
                if '.tga' in temp_string:
                    temp_string =  temp_string.split('=')[1].replace('"', '')
                    if finddup(leader_picture, temp_string) is False:
                        leader_picture.append(temp_string)
                        amountarr.append(1)
                    else:
                        index = leader_picture.index(temp_string)
                        amount = amountarr[index] + 1
                        amountarr[index] = amount
                elif '"' not in temp_string:
                    temp_string = temp_string.split(' ')[2]
                    if finddup(event_picture, temp_string) is False:
                        event_picture.append(temp_string)
                else:
                    temp_string = temp_string.split('=')[1].replace('"', '').strip()
                    if temp_string != "" and "." not in temp_string:
                        #print("Incorrect or false negative gfx key of " + temp_string + " at line " + line_number.__str__() + " in file " + file_name)
                        output_file.write("Incorrect or false negative gfx key of " + temp_string + " at line " + line_number.__str__() + " in file " + file_name + "\n")

    #GFX Keys that arent used
    event_gfx_key = []
    event_gfx_file_names_in_gfx_file = []
    file_names = listdir(interface_path)
    file_names.append("eventpictures.gfx")
    for file_name in file_names:
        if "event" in file_name and 'gfx' in file_name:
            line_number = 0
            if file_name != "eventpictures.gfx":
                file = open(interface_path + "\\" + file_name, 'r', 'utf-8')
            else:
                file = open(hoi4path + "\\interface\\" + file_name, 'r', 'utf-8')
            lines = file.readlines()
            for line in lines:
                line_number += 1
                if "name" in line and line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('"')[1].strip()
                    event_gfx_key.append(temp_string)
                    if finddup(event_picture, temp_string) is False:
                        #print("Unused Gfx: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name)
                        output_file.write("Unused event Gfx: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name + "\n")
                if "texturefile" in line and line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('"')[1].strip()
                    event_gfx_file_names_in_gfx_file.append(temp_string)
                    #print(temp_string)

    #GFX keys in events that arent initialised
    for file_name in listdir(event_path):
        line_number = 0
        file = open(event_path + "\\" + file_name, 'r', 'utf-8')
        lines = file.readlines()
        for line in lines:
            line_number += 1
            temp_string = line.strip()
            if "picture" in line and temp_string.startswith('#') is False:
                if '"' not in temp_string:
                    if '#' in temp_string:
                        temp_string = temp_string.split('#')[0].strip()
                    temp_string.replace('	', ' ')
                    temp_string = temp_string.split(' ')[2]
                    #print(temp_string)
                    if finddup(event_gfx_key, temp_string) is False:
                        output_file.write("GFX key not found: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name + "\n")
                        #print("GFX key not found: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name)

    #Scrub actual pictures to see if theyre defined in .gfx files
    actual_found_gfx = []
    for root, directories, filenames in walk(event_gfx_path):
        for filename in filenames:
            temp_string = path.join(root, filename)[len(file_path)+1:].replace('\\','/')
            actual_found_gfx.append(temp_string)
            if finddup(event_gfx_file_names_in_gfx_file, temp_string) is False:
                output_file.write("GFX not used in any .gfx file: " + temp_string + "\n")
                #print("GFX not used in any .gfx file: " + temp_string)


