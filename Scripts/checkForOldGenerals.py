from os import listdir
from openFile import open_file
from timedFunction import timed

#not updated to use os.path.join because this function is silly and probably won't be used in the future
@timed
def check_for_old_generals(path, output_file):
    check(path, output_file, "\\history\\countries", 'utf-8-sig')
    check(path, output_file, "\\events", 'utf-8-sig')
    check(path, output_file, "\\common\\national_focus", 'ansi')
    check(path, output_file, "\\common\\scripted_effects", 'ansi')


def check(path, output_file, sub_path, encoding):
    path += sub_path
    for filename in listdir(path):
        current_line = 0
        file = open_file(path + '\\' + filename)
        line = file.readline()
        current_line += 1
        ok = 0
        is_in_general = 0
        while line:
            if 'create_corps_commander' in line or 'create_field_marshal' in line:
                is_in_general = 1
            if "#mw thinks this is a land commander" in line:
                output_file.write(sub_path + '\\' + filename +
                                  " there's an unchanged KR general around line " + str(current_line) + '\n')
            if "skill =" in line and "#" not in line and is_in_general == 1:
                ok = 1
            if "attack_skill" in line or "defense_skill" in line \
                    or "planning_skill" in line or "logistics_skill" in line and ok == 1:
                ok = 0
                is_in_general = 0
            if "}" in line and ok == 1:
                output_file.write(sub_path + '\\' + filename +
                                  " there's an old general around line " + str(current_line) + '\n')
                is_in_general = 0
                ok = 0
            line = file.readline()
            current_line += 1


