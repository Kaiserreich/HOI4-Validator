import os
from openFile import open_file



def search_effects(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs):
    originalpath = path
    path = os.path.join(originalpath, "events")
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped, **kwargs)
    commonpath = os.path.join(originalpath, "common")
    path = os.path.join(commonpath, "national_focus")
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs)
    path = os.path.join(commonpath, "scripted_effects")
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings,thingstripped, **kwargs)
    path = os.path.join(commonpath, "decisions")
    maindict, linedict, filedict = create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs)
    return maindict, linedict, filedict

def create_search_dict(maindict, linedict, filedict, path, searchstrings, filterstrings, thingstripped, **kwargs):

    debug = False
    focussearch = False
    eventsearch = False
    techsearch = False
    needdepth = False
    decisionsearch = False
    skipfiles = []
    checkfiles = True
    try:
        skipfiles = kwargs.get('skipfiles')
        for name in skipfiles:
            break
        filterfiles = True
    except:
        filterfiles = False
    if thingstripped == 'lockey':
        if "id =" in searchstrings:
            focussearch = True
        elif 'events' in path:
            eventsearch = True
        elif 'technologies' in path:
            techsearch = True
        elif 'decisions' in path:
            decisionsearch = True
    if focussearch == True or techsearch == True or decisionsearch == True:
        needdepth = True
    for filename in os.listdir(path):
        shouldcontinue = False
        if ".txt" in filename or ".yml" in filename: #this makes sure it's not a folder
            if debug:
                print(filename)
            if filterfiles: #checking to make sure it's not in a file we're not supposed to check
                for name in skipfiles:
                    if name == filename:
                        #print("in should continue for " + filename)
                        shouldcontinue = True
            if checkfiles:
                try:
                    checkfile = kwargs.get('checkfiles')
                    if (checkfile in filename.lower()) == False:
                        shouldcontinue = True
                        if debug:
                            print("skipping this file")
                except:
                    if debug:
                        print("not checking files this time")
                    checkfiles = False
            if shouldcontinue == True:
                continue
            hasoccured = False
            eventyes = False
            current_line = 0
            file = open_file(os.path.join(path, filename))
            line = file.readline()
            current_line += 1
            eventdeep = 0
            nextline = False
            while line:
                line = line.split('#')[0] #this means it won't look at comments, if there are any comments
                i = 0
                foundstring = 0
                isin = False
                while i < len(searchstrings):
                    if needdepth:
                        if 'event' in line:
                            eventyes = True
                        if '{' in line:
                            eventdeep = eventdeep + line.count('{')
                    if searchstrings[i] in line:
                        try:
                            searchstrings2 = kwargs.get('searchstrings2')
                            for item in searchstrings2:
                                if item in line:
                                    isin = True
                                    foundstring = i
                        except TypeError:
                            foundstring = i
                            isin = True #checking to see if it has stuff that means it should be checked
                    if needdepth:
                        if '}' in line:
                            eventdeep = eventdeep - line.count('}')
                        if focussearch == True:
                            if eventyes == True:
                                isin = False
                            if eventdeep == 0:
                                eventyes = False
                        elif techsearch == True:
                            if eventdeep != 3:
                                isin = False
                            if nextline == True:
                                isin = True
                                foundstring = i
                        elif decisionsearch == True:
                            if eventdeep != 2:
                                isin = False
                    i = i+1
                i = 0
                while i < len(filterstrings):
                    if filterstrings[i] in line:
                        isin = False #checking to see if it's being filtered for one reason or another
                    i = i+1
                if nextline == True:
                    isin = True
                if isin:
                    #this means line is a thing being called, so we need to add it to the dictionary
                    if thingstripped == 'lockey':
                        if focussearch == True:
                            if hasoccured == True:
                                maintext = eventlocstrip(line)
                                if (maintext in maindict) == False and maintext != 'yes' and maintext != 'no':
                                    #print(maintext)
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path, desc=True)
                            else:
                                hasoccured = True
                        elif eventsearch == True:
                            maintext = line.split(' = ')[1].strip()
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                        elif techsearch == True:
                            if nextline == False:
                                #print("nextline to true")
                                nextline = True
                            else:
                                maintext = line.strip()
                                #print(maintext)
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path, desc=True)
                                nextline = False
                        elif decisionsearch == True:
                                maintext = line.split(' = {')[0].strip()
                                #print(maintext)
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path, desc=True)
                    elif thingstripped == 'oob':
                        maintext = stripOOB(line)
                        #print(maintext)
                        if maintext != 'empty' and maintext != "" and (maintext in maindict) == False:
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == 'states':
                        maintext = line.split(' = ')[1].strip()
                        if maintext.isdigit():
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == 'general':
                        maintext = stripGeneral(line)
                        if maintext != 'empty' and maintext != "" and (maintext in maindict) == False:
                            #print(maintext)
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == '=no':
                        maindict, linedict, filedict = insertdict(maindict, linedict, filedict, line, current_line, filename, path)
                    elif thingstripped == 'focus':
                        if 'has_completed_focus' in line:
                            maintext = strip_focus(line, 1, 'has_completed_focus =')
                            if (maintext in maindict) == False and maintext != "":
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                        else:
                            linelist = line.split(' focus =')
                            for posfocus in linelist:
                                maintext = strip_focus(posfocus, 0, '=')
                                if (maintext in maindict) == False and maintext != "":
                                    maindict, linedict, filedict = insertdict(maindict, linedict, filedict, maintext, current_line, filename, path)
                    elif thingstripped == 'ideology':
                        if debug:
                            print("line is " + line+" foundstring is " + str(foundstring))
                        text = line.split(searchstrings[foundstring])[1].split()[0].split('}')[0]
                        if debug:
                            print(text)
                        maindict, linedict, filedict = insertdict(maindict, linedict, filedict, text,
                                                                      current_line, filename, path)
                    elif thingstripped == "vp":
                        if nextline == False:
                            try:
                                text = line.split(searchstrings[0])[1].strip().split(' ')[1]
                                if debug:
                                    print(text)
                                maindict, linedict, filedict = insertdict(maindict, linedict, filedict, text,
                                                                          current_line, filename, path)
                            except:
                                nextline = True
                        else:
                            nextline = False
                            text = line.strip().split(' ')[0]
                            if debug:
                                print(text)
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, text,
                                                                          current_line, filename, path)
                    elif thingstripped == "vp_loc":
                            text = line.split(searchstrings[0])[1].strip().split(':')[0]
                            if debug:
                                print(text)
                            maindict, linedict, filedict = insertdict(maindict, linedict, filedict, text,
                                                                          current_line, filename, path)
                line = file.readline()
                current_line += 1
    return maindict, linedict, filedict

def eventlocstrip(line):
    maintext = line.split("id =")[1].strip()
    maintext = maintext.split(" ")[0].strip()
    return maintext

def insertdict(maindict, linedict, filedict, maintext, current_line, filename, path, **kwargs):
    maindict[maintext] = False
    linedict[maintext] = current_line
    filedict[maintext] = path + '\\' + filename
    if 'desc' in kwargs:
        newtext = maintext+"_desc"
        maindict[newtext] = False
        linedict[newtext] = current_line
        filedict[newtext] = path + '\\' + filename
    return maindict, linedict, filedict

def stripOOB(line):
    #if 'OTT' in line: Debug related code, ignore this
    #    print(line)
    if ("load_oob" in line):
        foundline = line.split("load_oob = ")[1].strip()
    elif ("OOB = " in line):
        foundline = line.split("OOB = ")[1].strip()
    else:
        foundline = line.split("oob = ")[1].strip()
    anewline = foundline.replace("load_oob = ", "")
    newline = anewline.replace("OOB = ","")
    newline = newline.replace("oob = ","")
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

def stripGeneral(line):
    if ("has_unit_leader" in line):
        foundline = line.split("has_unit_leader = ")[1].strip()
    else:
        foundline = line.split("remove_unit_leader = ")[1].strip()
    if(" }") in foundline:
        foundline = foundline.split(" }")[0].strip()
    return foundline

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