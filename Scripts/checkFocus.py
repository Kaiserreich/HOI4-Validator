from os import listdir
from openFile import open_file
from createDict import create_search_dict, strip_focus


def actually_check_for_missing_focus(path, focusdict):
    #this heads through the files. Every time it sees a focus, it sets that focus's value in returndict to true
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
    focusdict, linedict, filedict = create_search_dict(focusdict, linedict, filedict, path, ['focus = '], ['event', '.'], 'focus')
    finaldict = actually_check_for_missing_focus(path, focusdict)
    for key in finaldict:
        if finaldict[key] == False:
            result = "The focus " + key + " referenced in file " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)
