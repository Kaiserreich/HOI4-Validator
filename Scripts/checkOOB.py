from os import listdir
from openFile import open_file


def check_for_missing_OOB(path, output_file):
    originalpath = path
    #this creates a dict of all the oobs that are referenced
    path+="\\history\\countries"
    oobdict = {}
    linedict = {}
    filedict = {}
    oobdict, linedict, filedict = createOOBdict(oobdict, linedict, filedict, path)
    path = originalpath + "\\events"
    oobdict, linedict, filedict = createOOBdict(oobdict, linedict, filedict, path)
    path = originalpath + "\\common\\national_focus"
    oobdict, linedict, filedict = createOOBdict(oobdict, linedict, filedict, path)
    finaldict = actually_check_for_missing_oob(originalpath, oobdict)
    for key in finaldict:
        if finaldict[key] == False:
            result = "The oob " + key + " referenced in file " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)

def createOOBdict(oobdict, linedict, filedict, path):
    for filename in listdir(path):
        current_line = 0
        file = open_file(path + '\\' + filename)
        line = file.readline()
        current_line += 1
        while line:
            if ('OOB = ' in line or 'load_oob = ' in line):
                #this means line is oob being called, so we need to add it to the dictionary
                oobtext = stripOOB(line)
                if oobtext != 'empty' and '#' not in line:
                    #print(oobtext)
                    oobdict[oobtext] = False
                    linedict[oobtext] = current_line
                    filedict[oobtext] = filename
            line = file.readline()
            current_line += 1
    return oobdict, linedict, filedict

def stripOOB(line):
    if ("load_oob" in line):
        foundline = line.split("load_oob = ")[1].strip()
    else:
        foundline = line.split("OOB = ")[1].strip()
    anewline = foundline.replace("load_oob = ", "")
    newline = anewline.replace("OOB = ","")
    nextline = newline.replace("\"","")
    tfinalline = nextline.replace("\n","")
    removeeffect1 = tfinalline.replace("hidden_effect = { ", "")
    afinalline = removeeffect1.replace("}", "")
    mfinalline = afinalline.replace("add_equipment_to_stockpile = {", "")
    threefinalline = mfinalline.split("add_ideas")[0].strip()
    finalline = threefinalline.split("= {")[0].strip()
    lastline = finalline.strip()
    reallastline = lastline.split(" ")[0].strip()
    return reallastline

def actually_check_for_missing_oob(path, oobdict):
    returndict = oobdict
    path+="\\history\\units"
    for filename in listdir(path):
        returndict[filename.replace(".txt", "")] = True
    return returndict