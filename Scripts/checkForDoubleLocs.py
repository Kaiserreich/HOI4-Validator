from os import listdir
from codecs import open


 
def check_for_double_locs(path, output_file):
    path += "\\localisation"
    list_loc = {}
    for filename in listdir(path):
        current_line = 0
        file = open(path + '\\' + filename, 'r', 'utf-8-sig')
        line = file.readline()
        current_line += 1
        if "l_english" in line:
            line = file.readline()
            current_line += 1
            while line:
                line = line.strip()
                i = line.find(':')
                if i != -1:
                    loc = line[:i]
                    if loc in list_loc:
                        output_file.write("Duplicated Loc: '" + loc + "' in: " + list_loc[loc] + " and in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
                    else:
                        list_loc[loc] = "'\\localisation\\" + filename + "' at line " + str(current_line)
                    if "  " in line[i+1:]:
                        output_file.write("Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
                line = file.readline()
                current_line += 1