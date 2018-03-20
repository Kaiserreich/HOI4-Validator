from os import listdir
from codecs import open


def kr_check_for_old_generals(path, output_file):
    original_path = path
    path += "\\history\\countries"
    countries(path, output_file)
    path = original_path + "\\events"
    events(path, output_file)


def countries(path, output_file):
    for filename in listdir(path):
        current_line = 0
        file = open(path+'\\'+filename, 'r', 'utf-8-sig')
        line = file.readline()
        current_line += 1
        while line:
            if "#mw thinks this is a land commander" in line:
                output_file.write(path+ "\\" + filename +
                                  " there's an old general around line " + str(current_line) +'\n')
            line = file.readline()
            current_line += 1


def events(path, output_file):
    for filename in listdir(path):
        current_line = 0
        file = open(path + '\\' + filename, 'r', 'utf-8-sig')
        line = file.readline()
        current_line += 1
        ok = 0
        while line:
            if "skill =" in line and "#" not in line:
                ok = 1
            if "attack_skill" in line or "defense_skill" in line or "planning_skill" in line or "logistics_skill" in line and ok == 1:
                ok = 0
            if "}" in line and ok == 1:
                output_file.write(path + "\\" + filename +
                                  " there's an old general around line " + str(current_line) + '\n')
                ok = 0
            line = file.readline()
            current_line += 1

