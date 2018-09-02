from os import listdir
from openFile import open_file



def search_effects(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped):
    originalpath = path
    path = originalpath + "\\events"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped)
    path = originalpath + "\\common\\national_focus"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    path = originalpath + "\\common\\scripted_effects"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped)
    path = originalpath + "\\common\\decisions"
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    return maindict, linedict, filedict

def create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped):
    filterstrings.append('#') #ignore comments
    for filename in listdir(path):
        if ".txt" in filename: #this makes sure it's not a folder
            current_line = 0
            file = open_file(path + '\\' + filename)
            line = file.readline()
            current_line += 1
            while line:
                i = 0
                isin = False
                while i < len(searchstrings):
                    if searchstrings[i] in line:
                        isin = True #checking to see if it has stuff that means it should be checked
                    i = i+1
                i = 0
                while i < len(filterstrings):
                    if filterstrings[i] in line:
                        isin = False #checking to see if it's being filtered for one reason or another
                    i = i+1
                if isin:
                    #this means line is oob being called, so we need to add it to the dictionary
                    if thingstripped == 'oob':
                        maintext = stripOOB(line)
                        if maintext != 'empty' and maintext != "" and (maintext in maindict) == False:
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename)
                    elif thingstripped == 'focus':
                        if 'has_completed_focus' in line:
                            maintext = strip_focus(line, 1, 'has_completed_focus =')
                            if (maintext in maindict) == False and maintext != "":
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename)
                        else:
                            linelist = line.split(' focus =')
                            for posfocus in linelist:
                                maintext = strip_focus(posfocus, 0, '=')
                                if (maintext in maindict) == False and maintext != "":
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename)
                line = file.readline()
                current_line += 1
    return maindict, linedict, filedict

def insertdict(maindict, linedict, filedict, maintext, current_line, filename):
    maindict[maintext] = False
    linedict[maintext] = current_line
    filedict[maintext] = filename
    return maindict, linedict, filedict

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


def strip_focus(focustext, value, splittext):
    #this strips the focus of surrounding text
    #I made it because if I ever copy and paste code, it means I have failed
    finaltext = focustext.split(splittext)[value].strip()
    finaltext = finaltext.split(' ')[0].strip()
    finaltext = finaltext.split('\t')[0].strip()
    finaltext = finaltext.replace("}", "")
    finaltext = finaltext.replace("{", "")
    finaltext = finaltext.strip()
    if (finaltext == "no" or finaltext == "yes" or finaltext == "prerequisite" or finaltext == "if" or finaltext == "avalible" or finaltext == "bypass" or finaltext == "has_completed_focus" or finaltext == "mutually_exclusive" or finaltext == "limit" or finaltext == "focus" or finaltext == "shared_focus"):
        #is this a kludge? Yes. Does it work? Also yes.
        finaltext = ""
    return finaltext