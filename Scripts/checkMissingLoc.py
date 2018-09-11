from timedFunction import timed
from createDict import create_search_dict
from os import listdir
from openFile import open_file

@timed
def check_for_missing_loc(path, output_file):
    originalpath = path
    nodict = {}
    linedict = {}
    filedict = {}
    searchfocusstrings = ['id =']
    filterfocusstrings = ['event']
    searcheventstrings = ['title =', 'desc =', 'name =']
    filtereventstrings = ['\"', "set_province_name", "reset_state_name", "set_state_name","add_named_threat",'{ideology']
    thingstripped = 'lockey'
    loclist = find_locs(originalpath)
    path = originalpath +'\\common\\national_focus'
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searchfocusstrings, filterfocusstrings, thingstripped)
    path = originalpath +'\\events'
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searcheventstrings, filtereventstrings, thingstripped)
    for key in nodict:
        if (key in loclist) == False:
            result = "loc key " + key +" in file " +filedict[key] + " on line " + str(linedict[key]) + " is missing\n"
            #if ('focus' in filedict[key]) == False:
                #print(result)
            output_file.write(result)

def find_locs(path):
    path = path+"\\" + "localisation"
    loclist = []
    #print("finding scripted triggers")
    for filename in listdir(path):
        #print(filename)
        if '.yml' in filename:
            file = open_file(path + "\\" + filename)
            for line in file:
                if ':0' in line:
                    loc = line.split(':0')[0].strip()
                    loc = loc.strip()
                    #print(loc)
                    loclist.append(loc)
    return loclist