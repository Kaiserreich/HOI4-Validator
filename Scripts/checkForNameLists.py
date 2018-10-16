from os import listdir
from os import path
import re
from openFile import open_file
from timedFunction import timed

# Note that it will produce false positives for unused tags

@timed
def check_for_name_lists(file_path, output_file):
    unit_types = ["light_armor", "medium_armor", "heavy_armor", "modern_armor", "paratrooper",
                  "marine", "mountaineers", "infantry", "cavalry", "motorized", "mechanized"]
    tags = list()

    # Step 1: Read the custom battalion types

    aux_path = file_path + "\\common\\units"

    for filename in listdir(aux_path):
        if path.isfile(path.join(aux_path, filename)):
            file = open_file(path.join(aux_path, filename))
            line = file.readline()
            level = 0
            unitnameset = False
            while line:

                if level == 1:
                    split_line = re.split(' |\t', line)
                    for word in split_line:
                        if word.isalpha():
                            unit_name = word
                            unitnameset = True
                            break

                if level == 2 and "group =" in line and unitnameset:
                    if "support" not in line and unit_name not in unit_types:
                        unit_types.append(unit_name)

                if '{' in line:
                    level = level + 1

                if '}' in line:
                    level = level - 1

                line = file.readline()

    # Step 2: read ALL THE TAGS
    commonpath = path.join(file_path, "common")
    aux_path = path.join(commonpath, "country_tags")

    file = open_file(path.join(aux_path, "00_countries.txt"))
    line = file.readline()

    while line:
        split_line = re.split(' |\t', line)
        if '#' not in split_line[0]:
            if split_line[0].isalpha():
                tags.append(split_line[0])
        line = file.readline()

    # Step 3: create shadow name lists for all tags to be removed when found

    tag_name_lists = {}

    for tag in tags:
        tag_name_lists[tag] = {}
        for unit_type in unit_types:
            tag_name_lists[tag][unit_type] = 1

    # Step 4: Start reading namelist files, to remove unit types as needed

    aux_path = path.join(commonpath, 'units', 'names_divisions')
    for filename in listdir(aux_path):
        level = 0
        file = open_file(path.join(aux_path, filename))
        line = file.readline()
        current_tags = list()
        current_unit_types = list()

        while line:
            if 'division_types' in line:
                for unit_type in unit_types:
                    if unit_type in line:
                        current_unit_types.append(unit_type)

            if 'for_countries' in line:
                for tag in tags:
                    if tag in line:
                        current_tags.append(tag)

            if '{' in line:
                level = level + 1

            if '}' in line:
                level = level - 1

            if level == 0:
                for tag in current_tags:
                    for unit_type in current_unit_types:
                        tag_name_lists[tag][unit_type] = 0
                current_tags.clear()
            line = file.readline()

    for tag in tags:
        for unit_type in unit_types:
            if tag_name_lists[tag][unit_type] == 1:
                output_file.write(tag + " has no " + unit_type + " namelist\n")


