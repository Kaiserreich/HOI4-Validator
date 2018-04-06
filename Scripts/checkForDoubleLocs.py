from os import listdir
from codecs import open


def find_first(line):
    for i in range(0, len(line)):
        if line[i] != ' ' and line[i] != '\t':
            return i

def check_double_spaces(str):
    for i in range(0, len(str) - 1):
        if(str[i] == ' ' and str[i+1] == ' '):
            return True
    return False
def check_for_double_locs(path, output_file):
    path += "\\localisation"
    list_loc = {}
    for filename in listdir(path):
        current_line = 0
        file = open(path + '\\' + filename, 'r', 'utf-8-sig')
        line = file.readline()
        current_line += 1
        line = file.readline()
        current_line += 1
        while line:
            i = line.find(':')
            if i != -1:
                j = find_first(line)
                loc = line[j:i]
                if loc in list_loc:
                    output_file.write("Duplicated Loc: '" + loc + "' in: " + list_loc[loc] + " and in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
                else:
                    list_loc[loc] = "'\\localisation\\" + filename + "' at line " + str(current_line)
                if(check_double_spaces(line[i+1:])):
                    output_file.write("Double Spaces in Loc: '" + loc + "' in: '\\localisation\\" + filename + "' at line " + str(current_line) + "\n")
            line = file.readline()
            current_line += 1