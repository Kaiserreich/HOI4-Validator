from os import listdir
from openFile import open_file
from createDict import create_search_dict
from createDict import search_effects
from timedFunction import timed

@timed
def check_for_missing_OOB(path, output_file):
    originalpath = path
    #this creates a dict of all the oobs that are referenced
    oobdict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['OOB = ', 'load_oob = ','oob = ']
    filterstrings = []
    thingstripped = 'oob'
    path+="\\history\\countries"
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    oobdict, linedict, filedict =search_effects(oobdict, linedict, filedict, originalpath, searchstrings, filterstrings, thingstripped)
    finaldict = actually_check_for_missing_oob(originalpath, oobdict)
    for key in finaldict:
        if finaldict[key] == False:
            result = "The oob " + key + " referenced in file " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)

def actually_check_for_missing_oob(path, oobdict):
    returndict = oobdict
    path+="\\history\\units"
    for filename in listdir(path):
        returndict[filename.replace(".txt", "")] = True
    return returndict