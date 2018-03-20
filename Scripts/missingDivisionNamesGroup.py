from os import listdir
from codecs import open


def missing_divisions_names_group (path, output_file):
    path += "\\history\\units"
    for filename in listdir(path):
        file = open(path + '\\' + filename, 'r', 'ansi')
        line = file.readline()
        lines = 1
        while line:
            split_line = line.split(' ')
            level = 0
            entered_bracket = 0
            if 'division_template = {' in line:
                ok = 0
                start_line = lines
                while (not (entered_bracket == 1 and level == 0)) and line:
                    for string in split_line:
                        if "{" in string:
                            level += 1
                            entered_bracket = 1
                        if "}" in string:
                            level -= 1
                        if "division_names_group" in string:
                            if level != 1:
                                output_file.write("\\history\\units\\" + filename +
                                                  " division names group in wrong brackets at line:" + str(lines) + '\n')
                                ok = 2
                                break
                            else:
                                ok = 1
                    line = file.readline()
                    lines += 1
                    split_line = line.split(' ')

                if ok == 0 and entered_bracket == 1:
                    output_file.write("\\history\\units\\" + filename +
                                      " division names group missing at division starting on line:"
                                      + str(start_line) + '\n')
            if entered_bracket == 0:
                lines += 1
                line = file.readline()
