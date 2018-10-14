from timedFunction import timed
from createDict import create_search_dict
import os
from openFile import open_file

@timed
def check_for_missing_loc(path, output_file, searchdict):
    originalpath = path
    nodict = {}
    linedict = {}
    filedict = {}
    searchfocusstrings = ['id =']
    filterfocusstrings = ['event']
    searcheventstrings = ['title =', 'desc =', 'name =']
    filtereventstrings = ['\"', "set_province_name", "reset_state_name", "set_state_name","add_named_threat",'{ideology', '{ ideology']
    searchtechstrings = ['enable_equipments =']
    filtertechstrings = []
    searchdecisionstrings = ['= {']
    filterdecisionstrings = ['ai_will_do', 'allowed', 'modifier', 'available', 'visible', 'highlight_states', 'cancel_trigger']
    thingstripped = 'lockey'
    loclist = find_locs(originalpath)
    skipfiles = []
    if not searchdict['check_air_doctrine_loc']:
        skipfiles.append("air_doctrine.txt")
    if not searchdict['check_air_tech_loc']:
        skipfiles.append("air_techs.txt")
    if not searchdict['check_armor_loc']:
        skipfiles.append("armor.txt")
    if not searchdict['check_artillery_loc']:
        skipfiles.append("artillery.txt")
    if not searchdict['check_electro_mechanical_eng_loc']:
        skipfiles.append("electronic_mechanical_engineering.txt")
    if not searchdict['check_industry_loc']:
        skipfiles.append("industry.txt")
    if not searchdict['check_infantry_loc']:
        skipfiles.append("infantry.txt")
    if not searchdict['check_land_doctrine_loc']:
        skipfiles.append("land_doctrine.txt")
    if not searchdict['check_naval_loc']:
        skipfiles.append("naval.txt")
    if not searchdict['check_naval_doctrine_loc']:
        skipfiles.append("naval_doctrine.txt")
    if not searchdict['check_support_loc']:
        skipfiles.append("support.txt")
    commonpath = os.path.join(originalpath, 'common')
    path = os.path.join(commonpath, 'national_focus')
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searchfocusstrings, filterfocusstrings, thingstripped)
    path = os.path.join(originalpath, 'events')
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searcheventstrings, filtereventstrings, thingstripped)
    path = os.path.join(commonpath, 'technologies')
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searchtechstrings, filtertechstrings, thingstripped, skipfiles = skipfiles) #skipfiles is added so that way it can skip tech files that are identical to vanilla
    path = os.path.join(commonpath, 'decisions')
    nodict, linedict, filedict =create_search_dict(nodict, linedict, filedict, path, searchdecisionstrings, filterdecisionstrings, thingstripped)
    for key in nodict:
        if (key in loclist) == False:
            result = "loc key " + key +" in file " +filedict[key] + " on line " + str(linedict[key]) + " is missing\n"
            #if ('decision' in filedict[key]):
                #print(result)
            output_file.write(result)

def find_locs(path):
    path = os.path.join(path,"localisation")
    locset = {}
    #print("finding scripted triggers")
    for filename in os.listdir(path):
        #print(filename)
        if '.yml' in filename:
            file = open_file(os.path.join(path,filename))
            for line in file:
                if ':0' in line:
                    loc = line.split(':0')[0].strip()
                    loc = loc.strip()
                    #print(loc)
                    locset.add(loc)
    return locset