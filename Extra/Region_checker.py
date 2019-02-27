from codecs import open
import sys
from os import listdir
import time
import os
import re


def convert_oob():
    #C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRIRON\history\units\ENG.txt
    path = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\history\\units"
    path_2 = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRBU\\history\\units"

    path_3 = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\history\\countries"

    examine_path = path
    navies = set()
    uniquely_navies = set()

    for filename in listdir(examine_path):
        with open(os.path.join(examine_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()

            level = 0
            search = False
            others = False
            navy_pairs = dict() # Start line: end line
            temp_line = 0

            for line_number, line in enumerate(lines):

                if '#' in line:
                    if line.strip().startswith("#") is True:
                        continue
                    else:
                        line = line.split('#')[0]

                if 'navy' in line:
                    temp_line = line_number
                    search = True

                if "division" in line or "air_wings" in line:
                    others = True

                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

                if search is True and '}' in line and level == 1:
                    navy_pairs[temp_line] = line_number +1
                    search = False




            if(len(navy_pairs)) == 0:
                continue
            elif others is False:
                uniquely_navies.add("\"" + filename[:-4] + "\"")
            else:
                navies.add("\"" + filename[:-4] + "\"")

            start_numbers = list(navy_pairs.keys())
            end_numbers = list(navy_pairs.values())


            if others is True:
                with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
                    outputfile.truncate()

                    navy_file = open(os.path.join(examine_path, filename[:-4] + "_naval.txt"), 'w', 'utf-8-sig')
                    navy_file.truncate()

                    navy_file.write("### OOB for file " + filename + "\nunits = {\n")

                    other_file = False
                    inline = False
                    name = ""

                    for line_number, line in enumerate(lines):
                        if line_number in end_numbers:
                            inline = False
                            navy_file.write("\t}\n\n")
                            other_file = False
                        if line_number in start_numbers:
                            other_file = True


                        if other_file is False:
                            outputfile.write(line)
                        else:

                            if "navy" in line:
                                line = "\tfleet = {\n"
                                inline = False
                            if 'base' in line:
                                line = "\t\tnaval_base =" + line.split("=")[1]
                            if 'name' in line:
                                name = line.split("=")[1].strip()
                            if 'location' in line:
                                line = "\ttask_force = {\n\t\t\tname = " + name + "\n\t\t\t" + line.strip() + "\n"
                                inline = True

                            if inline:
                                line = "\t" + line

                            navy_file.write(line)

                    navy_file.write("}")
                    navy_file.close()
            else:
                with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
                    outputfile.truncate()

                    other_file = False
                    inline = False
                    name = ""

                    for line_number, line in enumerate(lines):
                        if line_number in start_numbers:
                            other_file = True
                        elif line_number in end_numbers:
                            inline = False
                            outputfile.write("\t}\n\n")
                            other_file = False

                        if other_file is False:
                            outputfile.write(line)
                        else:

                            if "navy" in line:
                                line = "\tfleet = {\n"
                            if 'base' in line:
                                line = "\t\tnaval_base =" + line.split("=")[1]
                            if 'name' in line:
                                name = line.split("=")[1].strip()
                            if 'location' in line:
                                line = "\ttask_force = {\n\t\t\tname = " + name + "\n\t\t\t" + line.strip() + "\n"
                                inline = True

                            if inline:
                                line = "\t" + line

                            outputfile.write(line)

    print(navies)
    print(uniquely_navies)

    examine_path = path_3
    for filename in listdir(examine_path):
        with open(os.path.join(examine_path, filename), 'r', 'utf-8-sig') as file:
            lines = file.readlines()

        with open(os.path.join(examine_path, filename), 'w', 'utf-8-sig') as outputfile:
            outputfile.truncate()

            for line_number, line in enumerate(lines):
                if 'oob' in line or 'OOB' in line:
                    if line.split("=")[1].strip() in navies:
                        line = line + "set_naval_oob = " + line.split("=")[1].strip()[:-1] + "_naval\"\n"
                    elif line.split("=")[1].strip() in uniquely_navies:
                        print(line.split("=")[1].strip())
                        line = "set_naval_oob = " + line.split("=")[1].strip()[:-1] + "_naval\"\n"
                outputfile.write(line)




def strat_region():
    path = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\map\\strategicregions"
    path_2 = "G:\\Games\\steamapps\\common\\Hearts of Iron IV\\map\\strategicregions"
    path_3 = "C:\\Users\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\map\\definition.csv"

    filenames = {"filename": "naval_terrain = x"}


    for filename in listdir(path_2):
        with open(os.path.join(path_2, filename), 'r', 'utf-8') as file:
            lines = file.readlines()
            for lineno, line in enumerate(lines):
                if 'naval_terrain' in line:
                    filenames[filename] = line.strip()

    ocean = set()
    files = list(filenames.keys())
    print(files)

    with open(path_3, 'r', 'utf-8') as file:
        lines = file.readlines()
        for lineno, line in enumerate(lines):
            stuff = line.strip().split(";")
            if stuff[6] == 'ocean':
                ocean.add(int(stuff[0]))



    for filename in listdir(path):
        with open(os.path.join(path, filename), 'r', 'utf-8') as file:
            lines = file.readlines()

        to_check = False

        for lineno, line in enumerate(lines):
            if 'provinces' in line:
                this_id = set([int(_) for _ in lines[lineno + 1].strip().split(" ") if _ not in ["", " "]])

                if ocean.intersection(this_id) != set():

                    if filename in files:
                        to_check = True
                    else:
                        print(filename)

            if 'naval_terrain' in line:
                to_check = False

        if to_check:
            with open(os.path.join(path, filename), 'w', 'utf-8') as outputfile:
                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    replacement_text = line

                    if 'weather' in line:
                        replacement_text = "\t" + filenames[filename] + "\n" + line

                    outputfile.write(replacement_text)

def tech():
    path_1 = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\common\\technologies"
    path_2 = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\common\\ideas"
    path_3 = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRIRON\\common\\country_leader"

    for path in [path_1, path_2, path_3]:
        for filename in listdir(path):
            with open(os.path.join(path, filename), 'r', 'utf-8') as file:
                lines = file.readlines()

            with open(os.path.join(path, filename), 'w', 'utf-8') as outputfile:

                outputfile.truncate()

                for line_number, line in enumerate(lines):

                    if line.strip().startswith('#'):
                        outputfile.write(line)
                        continue

                    replacement_text = line

                    if 'research_speed_factor' in line:

                        if '{' in line:
                            amount = float(line.split("=")[2].split("}")[0].split("#")[0].strip())
                        else:
                            amount = float(line.split("=")[1].split("}")[0].split("#")[0].strip())

                        if amount < 0.1000000001:
                            amount = round(-1*amount, 3)
                        else:
                            amount = round((1/(amount + 1))-1, 3)
                            replacement_text = line.split("research_speed_factor")[0] + "research_speed_factor = " + str(amount) + line.split('=')[1][6:]



                    outputfile.write(replacement_text)




def main():
    #strat_region()
    #tech()
    convert_oob()


if __name__ == "__main__":
    main()