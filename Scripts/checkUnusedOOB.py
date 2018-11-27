import os
from createDict import create_search_dict
from createDict import search_effects
from timedFunction import timed

@timed
def check_for_unused_OOB(path, output_file):
    originalpath = path
    #this creates a dict of all the oobs that exist
    oobdict = {}
    newoobdict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['OOB = ', 'load_oob = ', 'oob = ']
    filterstrings = []
    thingstripped = 'oob'
    path = os.path.join(path, 'history', 'countries')
    finaldict = actually_check_for_unused_oob(originalpath, newoobdict)
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    path = os.path.join(originalpath, 'common', 'technologies')
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    oobdict, linedict, filedict =search_effects(oobdict, linedict, filedict, originalpath, searchstrings, filterstrings, thingstripped)
    for key in oobdict:
        #print(key)
        finaldict[key] = True
    for key in finaldict:
        if finaldict[key] == False:
            result = "The oob " + key + " is not used by anything.\n"
            #print(result)
            output_file.write(result)

def actually_check_for_unused_oob(path, oobdict):
    returndict = oobdict
    path = os.path.join(path, 'history', 'units')
    for filename in os.listdir(path):
        oobname = filename.replace(".txt", "")
        if (oobname != 'empty'):
            returndict[oobname] = False
    return returndict