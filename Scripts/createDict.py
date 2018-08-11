from os import listdir
from openFile import open_file
def create_search_dict(oobdict, linedict, filedict, path, searchstrings, thingstripped):
    for filename in listdir(path):
        if ".txt" in filename:
            current_line = 0
            file = open_file(path + '\\' + filename)
            line = file.readline()
            current_line += 1
            while line:
                i = 0
                isin = False
                while i < len(searchstrings):
                    if searchstrings[i] in line:
                        isin = True
                    i = i+1
                if isin:
                    #this means line is oob being called, so we need to add it to the dictionary
                    if thingstripped == 'oob':
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
