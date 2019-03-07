from os import listdir
from os import walk
from os import path
from codecs import open
from timedFunction import timed

from openFile import open_file

@timed
def check_for_missing_gfx(file_path, output_file, hoi4_path):
    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess

    #Checklist:
    # Per type either check directly for file name or check for the keys in .gfx files
    # .gfx for
    #   Focus
    #   Events
    #   Ideas
    #   Decisions
    #Not needed to check for minister files, since its auto generated with filename.tga -> filename
    #
    #For each check:
    #   Picture used in key
    #   used gfx key never defined
    #   defined gfx key never used
    #Flags:
    #   Normal: Done
    #   Cosmetic: Done
    #Leader GFX:
    #   Events: Done
    #   Decisions: Done
    #   Focus Trees: Done
    #   History: Done
    #General GFX:
    #   Events: Done
    #   Decisions: Done
    #   Focus Trees: Done
    #   History: Done
    #Decisions:
    #   Icons: Actually Done
    #Event GFX:
    #   Events: Done
    #Tech GFX:
    #   Tech Trees:
    #Focus Icons:
    #   Focus Trees: Done
    #Idea Icons:
    #   Focus Trees:
    #   Decisions(?):
    #   Events:
    #Nation:
    #   Ministers: Done by mw
    #   Companies:
    #Other:
    #   Miscased: Done (Only relevant for leader portraits so far)

    common_path = path.join(file_path, "common")
    gfx_path = path.join(file_path, "gfx")
    interface_path = path.join(file_path, "interface")

    tree_path = path.join(common_path, "national_focus")
    tree_gfx_path =path.join(gfx_path, 'interface', 'goals')

    decisions_path = path.join(common_path, 'decisions')

    #scripted_triggers_path = file_path + "\\common\\scripted_effects"
    #Joke's on you, whoever wrote this script, I don't have to update this to work on linux if you never call it

    event_path = path.join(file_path, 'events')
    event_gfx_path =path.join(file_path, "event_pictures")

    #ideas_gfx_path = file_path + "\\gfx\\interface\\ideas"
    #ideas_gfx_path = file_path + "\\common\\ideas" #also for ministers

    #ministers_gfx_path = file_path + "\\gfx\\interface\\ministers"

    #tech_gfx_path = file_path + "\\gfx\\interface\\technologies"

    leaders_gfx_path = path.join(gfx_path, "leaders")
    country_history_path = path.join(file_path, 'history', 'countries')

    flags_gfx_path = path.join(gfx_path, "flags")

    check_flags(flags_gfx_path, output_file, file_path)

    check_a_lot(event_path, event_gfx_path,interface_path, file_path, output_file, hoi4_path, leaders_gfx_path, country_history_path, decisions_path, tree_path)

    focus_tree_icons(tree_path, hoi4_path, output_file, file_path, tree_gfx_path, interface_path)


def fill_tag_array(internal_path, cosmetics):
    # 0 = just normal
    # 1 = just cosmetic
    # 2 = both

    tags = []
    common_path = path.join(internal_path, "common")
    event_path = path.join(internal_path, 'events')
    tree_path = path.join(common_path, "national_focus")
    decisions_path = path.join(common_path, 'decisions')
    scripted_triggers_path = path.join(common_path, "scripted_effects")

    cosmetic_tag_dirs = [event_path, decisions_path, tree_path, scripted_triggers_path]

    #Find Normal Tags
    tags_path =path.join(path.join(common_path, 'country_tags'), '00_countries.txt')
    file = open_file(tags_path)
    #print("Reading: " + file.name)
    lines = file.readlines()

    if cosmetics != 1:
        for string in lines:
            temp_string = string[:3]
            if '#' in string:
                string = string.split('#')[0]
            if '#' not in temp_string and '\r\n' != string:
                tags.append(string[:3])
                #print("Found TAG: " + tags[counter])

    #Find Cosmetic Tags
    if cosmetics != 0:
        for dirs in cosmetic_tag_dirs:
            for filename in listdir(dirs):
                if 'categories' in filename:
                    continue
                file = open_file(path.join(dirs, filename))
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


def check_flags( flag_path, output_file, file_path, **kwargs):
    ideos = ["totalist", "syndicalist", "radical_socialist", "social_democrat", "social_liberal", "market_liberal", "social_conservative", "authoritarian_democrat", "paternal_autocrat", "national_populist"]
    flagarr = []
    medsmallword = ""
    if 'medsmall' in kwargs:
        medsmallword = " " + kwargs.get('medsmall')
    tag_array = fill_tag_array(file_path, 2)

    for file_name in listdir(flag_path):
        if 'medium' in file_name or 'small' in file_name:
            check_flags(path.join(flag_path, file_name), output_file, file_path, medsmall= file_name) #this calls the function again to make sure medium and small flags exist
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
            output_file.write("No"+ medsmallword+ "flag for " + strings + "\n")
            #print("No"+ medsmallword+ " flag for " + strings)


def check_a_lot(event_path, event_gfx_path, interface_path, file_path, output_file, hoi4path, leaders_gfx_path, country_history_path, decisions_path, tree_path):

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


    #Fill all the pictures (from events#)!
    amountarr = []
    event_picture = []
    leader_picture = []
    dirs = [country_history_path, event_path, tree_path, decisions_path]
    for dir in dirs:
        for file_name in listdir(dir):
            if 'categories' in file_name:
                continue
            line_number = 0
            file = open_file(path.join(dir, file_name))
            lines = file.readlines()
            for line in lines:
                line_number += 1
                if '#' in line:
                    line = line.split('#')[0].strip()
                if "picture" in line and line.strip().startswith('#') is False:
                    temp_string = line.strip()
                    if '.tga' in temp_string or '.dds' in temp_string:
                        temp_string = temp_string.split('=')[1].replace('"', '')
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
                file = open(path.join(interface_path, file_name), 'r', 'utf-8')
                vanilla = 0
            else:
                file = open_file(path.join(path.join(hoi4path, 'interface'), file_name))
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
        file = open_file(path.join(event_path, file_name))
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
    decisions_keys_full = []
    file = open(path.join(path.join(hoi4path, "interface"),"decisions.gfx"))
    lines = file.readlines()
    for line in lines:
        if '#' in line:
            line = line.split('#')[0].strip()
        if 'name' in line:
            if line.strip().startswith('#') is False:
                temp_string = line.split('\"')[1].strip()
                decisions_keys_full.append(temp_string)
                if 'category' in temp_string:
                    temp_string = temp_string[22:]
                else:
                    temp_string = temp_string[13:]
                decisions_keys.append(temp_string)
    for filenames in listdir(interface_path):
        if 'decisions' in filenames:
            file = open(path.join(interface_path,filenames))
            lines = file.readlines()
            for line in lines:
                if 'name' in line:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    if line.strip().startswith('#') is False:
                        temp_string = line.split('\"')[1].strip()
                        decisions_keys.append(temp_string[13:])
                        decisions_keys_full.append(temp_string)


    #Check Decision gfx in the txt files
    line_number = 0
    decisions_found = []
    pictures_found = []
    for filename in listdir(decisions_path):
        if 'categories' in filename:
            continue
        file = open(path.join(decisions_path,filename))
        lines = file.readlines()
        for line in lines:
            line_number += 1
            if 'icon' in line:
                if line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('=')[1].strip()
                    decisions_found.append(temp_string)
                    if finddup(decisions_keys, temp_string) is False:
                        if finddup(decisions_keys_full, temp_string) is False:
                            output_file.write("Didn't find icon decisions " + temp_string + " in file " + filename + " at " + line_number.__str__() + "\n")
                        else:
                            output_file.write("Key for decisions wrongly written (did you add or remove GFX_categories/GFX decisions)" + temp_string + " in file " + filename + " at " + line_number.__str__() + "\n")




    for filename in listdir(path.join(decisions_path, "categories")):
        file = open(path.join(path.join(decisions_path, "categories"), filename))
        lines = file.readlines()
        for line in lines:
            line_number += 1
            if 'icon' in line:
                if line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('=')[1].strip()
                    decisions_found.append(temp_string)
                    if finddup(decisions_keys, temp_string) is False:
                        if finddup(decisions_keys_full, temp_string) is False:
                            output_file.write("Didn't find icon decisions/ Wrong type used " + temp_string + " in file " + filename + " at " + line_number.__str__() + ". Did you forget to add categories_ to the icon name?\n")
                            #print("Didn't find icon decisions " + temp_string + " in file " + filename + " at " + line_number.__str__())
            if 'picture' in line:
                if line.strip().startswith('#') is False:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    temp_string = line.split('=')[1].strip()
                    decisions_found.append(temp_string)
                    if finddup(decisions_keys_full, temp_string) is False:
                        output_file.write("Didn't find icon decisions/ Wrong type used " + temp_string + " in file " + filename + " at " + line_number.__str__() + ". Did you forget to add categories_ to the icon name?\n")
                        #print("Didn't find picture decisions " + temp_string + " in file " + filename + " at " + line_number.__str__())


    #Check if KReys are used
    for filenames in listdir(interface_path):
        if 'decisions' in filenames:
            file = open(path.join(interface_path, filenames))
            lines = file.readlines()
            for line in lines:
                if 'name' in line:
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    if line.strip().startswith('#') is False:
                        temp_string = line.split('\"')[1].strip()
                        #temp_string = temp_string[13:]
                        if finddup(decisions_found, temp_string) is False:
                            if finddup(decisions_found, temp_string[13:]) is False:
                                #print("Found Unused KR Decision GFX " + temp_string + " in " + filenames)
                                output_file.write("Found Unused KR Decision GFX " + temp_string + " in " + filenames + "\n")

def focus_tree_icons(tree_path, hoi4_path, output_file, mod_path, tree_gfx, gfx_files):
    #First check if every file is defined

    #Fill all present goal icons
    tree_gfx_files = []
    for filename in listdir(tree_gfx):
        tree_gfx_files.append(filename)

    #Fill all defined keys from the .gfx file
    #KR specifically generates a shine file, so i will ignore that
    goals_files_needed = []
    gfx_names = []
    for filename in listdir(gfx_files):
        if 'goals' in filename and 'shine' not in filename:
            file = open(path.join(gfx_files, filename), 'r', 'utf-8')
            lines = file.readlines()
            for line in lines:
                if 'GFX_focus_jap_zero' in line:
                    print(line + ", " + filename)
                if 'name' in line:
                    temp_string = line.strip()
                    if temp_string.startswith('#'):
                        continue
                    if '#' in temp_string:
                        temp_string = temp_string.split('#')[0].strip()
                    temp_string = temp_string.split('"')[1]
                    gfx_names.append(temp_string)
                if 'texturefile' in line and 'shine_overlay' not in line:
                    temp_string = line.strip()
                    if temp_string.startswith('#'):
                        continue
                    if '#' in temp_string:
                        temp_string = temp_string.split('#')[0].strip()
                    temp_string = temp_string.split('"')[1]
                    if '/' in temp_string:
                        if 'goals' not in temp_string:
                            continue
                        temp_string = temp_string.split('/')[len(temp_string.split('/'))-1]
                    goals_files_needed.append(temp_string[:len(temp_string)-4])
                    if finddup(tree_gfx_files, temp_string) is False:
                        if 'tga' in temp_string:
                            if finddup(tree_gfx_files, temp_string.replace('tga', 'dds')) is False:
                                #print("Could not find " + temp_string + " in the gfx/interface/goals folder")
                                output_file.write("Could not find " + temp_string + " in the gfx/interface/goals folder\n")
                        elif 'dds' in temp_string:
                            if finddup(tree_gfx_files, temp_string.replace('dds', 'tga')) is False:
                                #print("Could not find " + temp_string + " in the gfx/interface/goals folder")
                                output_file.write("Could not find " + temp_string + " in the gfx/interface/goals folder\n")

    for filename in tree_gfx_files:
        if finddup(goals_files_needed, filename[:len(filename)-4]) is False:
            #print("Found focus texture not used " + filename[:len(filename)-4])
            output_file.write("Found focus texture not used " + filename[:len(filename)-4] + "\n")

    kr_gfx_names = gfx_names.copy()
    #append vanilla stuff
    file.close()
    file = open(path.join(path.join(hoi4_path, "interface"), "goals.gfx"), 'r', 'utf-8')
    lines = file.readlines()
    for line in lines:
        if 'name' in line:
            line = line.strip()
            if '#' in line:
                if line.startswith('#'):
                    continue
                else:
                    line = line.split('#')[0]
            line = line.split('"')[1]
            gfx_names.append(line)


    #start scrubbing
    found_gfx_in_tree = []
    for filename in listdir(tree_path):
        size = path.getsize(path.join(tree_path, filename))
        if size < 100:
            continue
        file = open_file(path.join(tree_path, filename))
        lines = file.readlines()
        line_number = 0
        for line in lines:
            line_number += 1
            if 'icon' in line:
                if '#' in line:
                    if line.startswith('#'):
                        continue
                    else:
                        line = line.split('#')[0]
                if line.strip() is not "" and '=' in line:
                    line = line.split('=')[1].strip()
                    found_gfx_in_tree.append(line)
                    if finddup(gfx_names, line) is False:
                        output_file.write("Found focus icon \"" + line + "\" not declared in " + filename + " in line: " + line_number.__str__() +"\n")

    for string in kr_gfx_names:
        if finddup(found_gfx_in_tree, string) is False:
            output_file.write("Found focus icon never used in any focus tree: " + string + "\n")
