from os import listdir
from openFile import open_file
from createDict import create_search_dict

def check_for_missing_OOB(path, output_file):
    originalpath = path
    #this creates a dict of all the oobs that are referenced
    path+="\\history\\countries"
    oobdict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['OOB = ', 'load_oob = ']
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, 'oob')
    path = originalpath + "\\events"
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, 'oob')
    path = originalpath + "\\common\\national_focus"
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, 'oob')
    path = originalpath + "\\common\\scripted_effects"
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, 'oob')
    path = originalpath + "\\common\\decisions"
    oobdict, linedict, filedict = create_search_dict(oobdict, linedict, filedict, path, searchstrings, 'oob')
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