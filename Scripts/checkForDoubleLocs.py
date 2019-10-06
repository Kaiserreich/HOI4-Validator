import os
from timedFunction import timed
from openFile import open_file
import re


def check_and_strip(string):
    return re.search(r"(^|[^\s])\s{2}($|[^\s])", string)


@timed
def check_for_double_locs(path, output_file, check_double_loc = True, check_double_spaces = True):
    path = os.path.join(path, "localisation")
    list_loc = {}
    subfolderlist = []
    for filename in os.listdir(path):
        if '.yml' in filename:
            file = open_file(os.path.join(path, filename))
            list_loc = linecheck(file, output_file, filename, list_loc, '', check_double_loc, check_double_spaces)
        else:
            subfolderlist.append(filename)
    for subfolder in subfolderlist:
        newpath = os.path.join(path, subfolder)
        for filename in os.listdir(newpath):
            if '.yml' in filename:
                file = open_file(os.path.join(newpath,filename))
                list_loc = linecheck(file, output_file, filename, list_loc, subfolder, check_double_loc, check_double_spaces)

def linecheck(file, output_file, filename, list_loc, subfolder, check_double_loc, check_double_space):
    if subfolder != '':
        subfolder = subfolder + '\\'
    current_line = 0
    line = file.readline()
    current_line += 1
    if "l_english" in line:
        line = file.readline()
        current_line += 1
        while line:
            line = line.strip()
            i = line.find(':')
            if i != -1 and line[0] != '#':
                loc = line[:i]
                if check_double_loc:
                    if loc in list_loc:
                        output_file.write("Duplicated Loc: '" + loc + "' in: " + list_loc[
                            loc] + " and in: '\\localisation\\" + subfolder +filename + "' at line " + str(current_line) + "\n")
                    else:
                        list_loc[loc] = "'\\localisation\\" + subfolder + filename + "' at line " + str(current_line)
                # if "  " in line[i+1:]:
                if check_double_space:
                    if check_and_strip(line):
                        # print("Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(current_line))
                        output_file.write(
                            "Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(
                                current_line) + "\n")
            line = file.readline()
            current_line += 1
    return list_loc