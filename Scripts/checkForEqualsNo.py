from createDict import create_search_dict
from timedFunction import timed
from openFile import open_file
from os import listdir


@timed

def check_for_equals_no(path, output_file):
    originalpath = path
    nodict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['= no']
    filterstrings = []
    thingstripped = '=no'
    triggerlist = find_scripted_triggers(originalpath)
    path = originalpath + "\\common\\national_focus"
    nodict, linedict, filedict = create_search_dict(nodict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, searchstrings2 = triggerlist)
    path = originalpath + "\\common\\decisions"
    nodict, linedict, filedict = create_search_dict(nodict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, searchstrings2 = triggerlist)
    for key in nodict:
        result = "= no is used in file " + filedict[key] + " on line " + str(linedict[key]) + ". Don't do that.\n"
        print(result)
        output_file.write(result)


def find_scripted_triggers(path):
    path += "\\common\\scripted_triggers"
    triggerlist = []
    print("finding scripted triggers")
    for filename in listdir(path):
        #print(filename)
        if '.txt' in filename:
            file = open_file(path + "\\" + filename)
            depth = 0;
            for line in file:
                if depth == 0 and '=' in line:
                    trigger = line.split('=')[0].strip()
                    if ("#" in trigger) == False:
                        #print(trigger)
                        triggerlist.append(trigger)
                if '{' in line:
                    depth = depth + 1
                if '}' in line:
                    depth = depth - 1
    return triggerlist
