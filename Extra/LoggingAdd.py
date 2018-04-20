from codecs import open
import sys
from os import listdir
import fileinput


def check_triggered(line_number, lines):
    if line_number == len(lines) or line_number == len(lines)-1:
        return True
    if '}' in lines[line_number+1]:
        #print("1: Found Triggered Event at line: " + line_number.__str__())
        return True
    for i in range(line_number, len(lines)):
        string = lines[i].strip()
        if string.startswith('#') is True:
            continue
        if string.startswith('}') is True:
            #print("2: Found Triggered Event at line: " + i.__str__())
            return True
        elif string != "":
            #print("3: Found normal Event at line: " + i.__str__())
            return False
    return False


def focus(cpath):
    #immediate = {log = "Focus id: "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\common\\national_focus"):
        if ".txt" in filename and ".bak" not in filename:
            file = open(cpath + "\\common\\national_focus\\" + filename, 'r', 'utf-8')
            lines = file.readlines()
            line_number = 0
            ids = []
            idss = []
            new_focus = False
            for line in lines:
                line_number += 1
                if line.strip().startswith('#') is True:
                    continue
                if 'focus = {' in line:  # New Event
                    new_focus = True
                if 'id' in line and new_focus is True:
                        focus_id = line.split('=')[1].strip()
                        if '#' in focus_id:
                            focus_id = focus_id.split('#')[0].strip()
                        ids.append(focus_id)
                if 'completion_reward' in line and new_focus is True:
                    new_focus = False
                    idss.append(line_number)

            line_number = 0
            outputfile = open(cpath + "\\common\\national_focus\\" + filename, 'w', 'utf-8')
            for line in lines:
                line_number += 1
                if line_number in idss:
                    event_id = ids[idss.index(line_number)]
                    replacement_text = "completion_reward = {\nlog = \"[Root.GetName]: Focus " + event_id + "\"#Auto-logging\n"
                    outputfile.write(line.replace("completion_reward = {", replacement_text))
                else:
                    outputfile.write(line)

def event(cpath):
    # immediate = {log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\events"):
        if ".txt" in filename and ".bak" not in filename:
            file = open(cpath + "\\events\\" + filename, 'r', 'utf-8-sig')
            lines = file.readlines()
            event_id = None
            line_number = 0
            triggered = False
            ids = []
            for line in lines:
                line_number += 1
                if 'country_event' in line: #New Event
                    if check_triggered(line_number, lines) is False:
                        new_event = True
                        if event_id is not None:
                            triggered = False
                    else:
                        triggered = True
                        new_event = False
                if 'id' in line and new_event is True:
                    if triggered is False:
                        new_event = False
                        event_id = line.split('=')[1].strip()
                        ids.append(line_number)
                    else:
                        triggered = False

            line_number = 0
            outputfile = open(cpath + "\\events\\" + filename, 'w', 'utf-8-sig')
            for line in lines:
                line_number += 1
                if line_number in ids:
                    event_id = line.split('=')[1].strip()
                    if '#' in event_id:
                        event_id = event_id.split('#')[0].strip()
                    replacement_text = event_id + "\n    immediate = {log = \"[Root.GetName]: event " + event_id  + "\"}#Auto-logging"
                    outputfile.write(line.replace(event_id, replacement_text))
                else:
                    outputfile.write(line[:-1])


def main():
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string
    event(cpath)
    focus(cpath)


if __name__ == "__main__":
    main()