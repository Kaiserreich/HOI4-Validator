from os import listdir
from openFile import open_file

def strip_focus(focustext, striptext):
    #this strips the focus of surrounding text
    #I made it because if I ever copy and paste code, it means I have failed
    finalstrip = striptext + " = "
    focustemp = focustext.replace(finalstrip, "")
    finaltext = focustemp.replace(" ", "")
    return finaltext

def actually_check_for_missing_focus(path, focusdict):
    #this heads through the files. Every time it sees a focus, it sets that focus's value in returndict to true
    returndict = focusdict
    for filename in listdir(path):
        file = open_file(path + '\\' + filename)
        line = file.readline()
        while line:
            if 'id = ' in line:
                focustext = strip_focus(line, 'id = ')
                returndict[focustext] = True
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
            if 'focus = ' in line:
                #this means line is focus being called, so we need to add it to the dictionary
                focustext = strip_focus(line, 'focus = ')
                #checking to make sure the focus isn't already in the dictionary
                if focusdict[focustest] == None:
                    focusdict[focustext] = False
                    linedict[focustext] = current_line
                    filedict[focustext] = filename
    finaldict = actually_check_for_missing_focus(path, focusdict)
    for key in finaldict:
        if finaldict[key] == False:
            output_file.write("The focus " + key + " referenced in file + " + filedict[key] + " on line " + linedict[key] + "doesn't actually exist. You should do something about that.")
