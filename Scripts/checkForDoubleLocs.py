from os import listdir
import time
from openFile import open_file


def check_and_strip(string, _range):
    for __range in range(_range, len(string)-2):
        if "  " in string[__range:__range+2] and (__range > 1 and " " not in string[__range-1:__range]) \
                and ((__range+2 < len(string) and " " not in string[__range+2:__range+3]) or
                     (__range+2 >= len(string))):
            return True
    return False

def check_for_double_locs(path, output_file):
    t0 = time.time()
    path += "\\localisation"
    list_loc = {}
    for filename in listdir(path):
        current_line = 0
        file = open_file(path + '\\' + filename)
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
                    if loc in list_loc:
                        output_file.write("Duplicated Loc: '" + loc + "' in: " + list_loc[loc] + " and in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
                    else:
                        list_loc[loc] = "'\\localisation\\" + filename + "' at line " + str(current_line)
                    #if "  " in line[i+1:]:
                    if check_and_strip(line, i) is True:
                        #print("Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(current_line))
                        output_file.write("Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
                line = file.readline()
                current_line += 1    
    t0 = time.time() - t0
    print("Time taken for Locs script: " + (t0*1000).__str__() + " ms")