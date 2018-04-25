from os import listdir
from openFile import open_file

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

def actually_check_for_missing_focus(path, focusdict):
    #this heads through the files. Every time it sees a focus, it sets that focus's value in returndict to true
    #it also makes sure the focus isn't commented out
    returndict = focusdict
    for filename in listdir(path):
        file = open_file(path + '\\' + filename)
        line = file.readline()
        while line:
            if 'id = ' in line and ('event' in line) == False and ('.' in line) == False:
                focustext = strip_focus(line, 1, '=')
                returndict[focustext] = True
            line = file.readline()
    return returndict

def check_for_missing_focus(path, output_file):
    #this creates a dict of all the focuses that are referenced
    path+="\\common\\national_focus"
    focusdict = {}
    linedict = {}
    filedict = {}
    for filename in listdir(path):
        current_line = 0
        file = open_file(path + '\\' + filename)
        line = file.readline()
        current_line += 1
        while line:
            if ('focus = ' in line) and ('event' in line) == False and ('.' in line) == False and ('#' in line) == False:
                #this means line is focus being called, so we need to add it to the dictionary
                if 'has_completed_focus' in line:
                    focustext = strip_focus(line, 1, 'has_completed_focus =')
                    if (focustext in focusdict) == False and focustext != "":
                        focusdict[focustext] = False
                        linedict[focustext] = current_line
                        filedict[focustext] = filename
                else:
                    linelist = line.split(' focus =')
                    for posfocus in linelist:
                        focustext = strip_focus(posfocus, 0, '=')
                        #checking to make sure the focus isn't already in the dictionary and that there's any text left after the strip
                        if (focustext in focusdict) == False and focustext != "":
                            focusdict[focustext] = False
                            linedict[focustext] = current_line
                            filedict[focustext] = filename
            line = file.readline()
            current_line += 1
    finaldict = actually_check_for_missing_focus(path, focusdict)
    for key in finaldict:
        if finaldict[key] == False:
            result = "The focus " + key + " referenced in file " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)
