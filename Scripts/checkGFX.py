from os import listdir
from os import walk
from os import path
from codecs import open
import time


def check_for_missing_gfx(file_path, output_file, hoi4_path):
    t0 = time.time()

    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess

    #Checklist:
    # Per type either check directly for file name or check for the keys in .gfx files
    # .gfx for
    #   Focus
    #   Events
    #   Ideas
    #   Companies
    #Not needed to check for minister files, since its auto generated with filename.tga -> filename
    #
    #For each check:
    #   Picture used in key
    #   used gfx key never defined
    #   defined gfx key never used
    #Flags:
    #   Normal: Done
    #   Cosmetic: Done
    #Leader/General GFX:
    #   Events: Done
    #   Decisions:
    #   Focus Trees(?):
    #Decisions:
    #   Icons: Done
    #Event GFX:
    #   Events: Done
    #Tech GFX:
    #   Tech Trees:
    #Focus Icons:
    #   Focus Trees:
    #Idea Icons:
    #   Focus Trees:
    #   Decisions(?):
    #   Events:
    #Nation:
    #   Ministers: Done by mw
    #   Companies:
    #Other:
    #   Miscased: Done

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

    check_events(event_path, event_gfx_path,interface_path, file_path, output_file, hoi4_path, leaders_gfx_path, country_history_path, decisions_path)
    t0 = time.time() - t0
    print("GFX script Time: " + (t0*1000).__str__() + " ms")


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


def strip_and_clean(string):
    if '/' in string:
        strings = string.split('/')
        return strings[len(strings)-1].strip()
    else:
        return string.strip()


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


def check_events(event_path, event_gfx_path, interface_path, file_path, output_file, hoi4path, leaders_gfx_path, country_history_path, decisions_path):

    #Scrub for leader gfx
    actual_found_portrait_gfx = []
    actual_found_portrait_gfx_lower = []
    actual_amount = []
    for root, directories, filenames in walk(leaders_gfx_path):
        for filename in filenames:
            #temp_string = path.join(root, filename)[len(file_path)+1:].replace('\\','/')
            temp_string = filename
            if finddup(actual_found_portrait_gfx, temp_string) is False:
                actual_found_portrait_gfx.append(temp_string)
                actual_found_portrait_gfx_lower.append((temp_string.lower()))
                actual_amount.append(1)
            else:
                index = actual_found_portrait_gfx.index(temp_string)
                amount = actual_amount[index] + 1
                actual_amount[index] = amount
                #print("Found Leader Portrait: " + temp_string + ", " + amount.__str__())

    #Scrub for leader gfx in vanilla
    for root, directories, filenames in walk(hoi4path + "\\gfx\\leaders"):
        for filename in filenames:
            #temp_string = path.join(root, filename)[len(file_path)+1:].replace('\\','/')
            temp_string = filename
            if finddup(actual_found_portrait_gfx, temp_string) is False:
                #print("Found Leader Portrait: " + temp_string)
                actual_found_portrait_gfx.append(temp_string)
                actual_found_portrait_gfx_lower.append((temp_string.lower()))
                actual_amount.append(1)
            else:
                index = actual_found_portrait_gfx.index(temp_string)
                amount = actual_amount[index] + 1
                actual_amount[index] = amount
                #print("Found Leader Portrait: " + temp_string + ", " + amount.__str__())


    #Fill all the pictures!
    amountarr = []
    event_picture = []
    leader_picture = []
    counter = 0
    dirs = [country_history_path, event_path]
    for dir in dirs:
        for file_name in listdir(dir):
            line_number = 0
            file = open(dir + "\\" + file_name, 'r', 'utf-8')
            lines = file.readlines()
            for line in lines:
                line_number += 1
                if "picture" in line and line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.strip()
                    if '.tga' in temp_string or '.dds' in temp_string:
                        temp_string =  temp_string.split('=')[1].replace('"', '')
                        if finddup(leader_picture, temp_string) is False:
                            temp_string = strip_and_clean(temp_string)
                            #print(temp_string)
                            leader_picture.append(temp_string)
                            amountarr.append(1)
                        else:
                            index = leader_picture.index(temp_string)
                            amount = amountarr[index] + 1
                            amountarr[index] = amount
                        if finddup(actual_found_portrait_gfx, temp_string) is False:
                            if finddup(actual_found_portrait_gfx_lower, temp_string.lower()) is True:
                                #print("Wrongly spelled portrait: " + temp_string + " in file " + dir.split('\\')[len(dir.split('\\'))-1] + "\\" + file_name + " at line " + line_number.__str__())
                                output_file.write("Wrongly spelled portrait: " + temp_string + " in  file " + dir.split('\\')[len(dir.split( '\\')) - 1] + "\\" + file_name + " at line " + line_number.__str__() + "\n")
                            else:
                                #print("Didnt find portrait: " + temp_string + " in file " + dir.split('\\')[len(dir.split('\\'))-1] + "\\" + file_name + " at line " + line_number.__str__())
                                output_file.write("Didnt find portrait: " + temp_string + " in  file " + dir.split('\\')[len(dir.split('\\')) - 1] + "\\" + file_name + " at line " + line_number.__str__() + "\n")
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
                vanilla = 0
            else:
                file = open(hoi4path + "\\interface\\" + file_name, 'r', 'utf-8')
                vanilla = 1
            lines = file.readlines()
            for line in lines:
                line_number += 1
                if "name" in line and line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('"')[1].strip()
                    if finddup(event_gfx_key, temp_string) is True:
                        #print("Duplicated gfx key " + temp_string +" in file " + file_name + " at line " + line_number.__str__())
                        output_file.write("Duplicated gfx key " + temp_string +" in file " + file_name + " at line " + line_number.__str__() + "\n")
                    else:
                        event_gfx_key.append(temp_string)
                    if finddup(event_picture, temp_string) is False and vanilla == 0:
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
                        output_file.write("GFX event key not found: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name + "\n")
                        #print("GFX key not found: " + temp_string + " at line " + line_number.__str__() + " in file " + file_name)

    #Scrub actual pictures to see if theyre defined in .gfx files
    actual_found_event_gfx = []
    for root, directories, filenames in walk(event_gfx_path):
        for filename in filenames:
            temp_string = path.join(root, filename)[len(file_path)+1:].replace('\\','/')
            if finddup(actual_found_event_gfx, temp_string) is True:
                #print("Duplicate event gfx: " + filename)
                output_file.write("Duplicate event gfx: " + temp_string + "\n")
            else:
                actual_found_event_gfx.append(temp_string)
            if finddup(event_gfx_file_names_in_gfx_file, temp_string) is False:
                output_file.write("GFX not used in any .gfx file: " + temp_string + "\n")
                #print("GFX not used in any .gfx file: " + temp_string)

    #Fill Decisions keys
    decisions_keys = []
    file = open(hoi4path + "\\interface\\decisions.gfx")
    lines = file.readlines()
    for line in lines:
        if 'name' in line:
            if line.strip().startswith('#') is False:
                temp_string = line.split('\"')[1].strip()
                decisions_keys.append(temp_string[13:])
    for filenames in listdir(interface_path):
        if 'decisions' in filenames:
            file = open(interface_path + "\\" + filenames)
            lines = file.readlines()
            for line in lines:
                if 'name' in line:
                    if line.strip().startswith('#') is False:
                        temp_string = line.split('\"')[1].strip()
                        decisions_keys.append(temp_string[13:])


    #Check Decision gfx in the txt files
    line_number = 0
    decisions_found = []
    for filename in listdir(decisions_path):
        if 'categories' in filename:
            continue
        file = open(decisions_path + "\\" + filename)
        lines = file.readlines()
        for line in lines:
            line_number += 1
            if 'icon' in line:
                if line.strip().startswith('#') is False:
                    temp_string = line.split('=')[1].strip()
                    decisions_found.append(temp_string)
                    if finddup(decisions_keys, temp_string) is False:
                        output_file.write("Didn't find icon decisions/" + temp_string + " in file " + filename + " at " +line_number.__str__() + "\n")

