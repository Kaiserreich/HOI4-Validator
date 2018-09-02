from os import listdir
from openFile import open_file
from createDict import stripGeneral
from createDict import search_effects
from timedFunction import timed

@timed
def check_for_missing_General(path, output_file):
    originalpath = path
    #this creates a dict of all the generals that are referenced
    generaldict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['has_unit_leader = ', 'remove_unit_leader =']
    filterstrings = []
    thingstripped = 'general'
    generaldict, linedict, filedict =search_effects(generaldict, linedict, filedict, originalpath, searchstrings, filterstrings, thingstripped)
    finaldict = actually_check_for_missing_general(originalpath, generaldict)
    for key in finaldict:
        if finaldict[key] == False:
            result = "The leader " + key + " referenced in file " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)

def actually_check_for_missing_general(originalpath, generaldict):
    #this heads through the files. Every time it sees a general, it sets that general's value in returndict to true
    pathlist = [originalpath+"\\history\\countries", originalpath + "\\events", originalpath + "\\common\\national_focus", originalpath + "\\common\\scripted_effects", originalpath + "\\common\\decisions"]
    returndict = generaldict
    SettingTraits = False
    for path in pathlist:
        for filename in listdir(path):
            if ".txt" in filename:
                file = open_file(path + '\\' + filename)
                line = file.readline()
                ingeneral = False
                while line:
                    if ingeneral == False:
                        if 'create_corps_commander' in line or 'create_field_marshal' in line or 'create_navy_leader' in line:
                            ingeneral = True
                    else:
                        if 'traits =' in line:
                            SettingTraits = True
                        if '}' in line:
                            if SettingTraits == False:
                                ingeneral = False
                            else:
                                SettingTraits = False
                        if 'id =' in line:
                            generalid = strip_created_general(line)
                            if generalid != '':
                                #print(ingeneral)
                                #print(path + '\\' + filename)
                                #print(generalid)
                                returndict[generalid] = True
                            ingeneral = False
                    line = file.readline()
    return returndict

def strip_created_general(line):
    #print(line)
    line = line.split("#")[0].strip()
    if 'id =' in line:
        line = line.split("id =")[1].strip()
    return line