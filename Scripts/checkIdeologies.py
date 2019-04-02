import os
from createDict import search_effects
from timedFunction import timed
from openFile import open_file

@timed
def check_ideologies(path, usesvanilla, output_file):
    debug = False
    ideologydict = {}
    linedict = {}
    filedict = {}
    defaultideologies = ['democratic', 'communism','fascism', 'neutrality']
    filterstrings = []
    thingstripped = 'ideology'
    searchstrings = ['ideology = ', 'has_government =', 'ruling_party = ']
    ideologydict, linedict, filedict = search_effects(ideologydict, linedict, filedict, path, searchstrings, filterstrings, thingstripped)
    ideologypath = os.path.join(path, 'common', 'ideologies')
    file = open_file(os.path.join(ideologypath, '00_ideologies.txt'))
    line = file.readline()
    depth = 0
    istypes = False
    ideologydict['ROOT'] = True
    if usesvanilla:
        for each in defaultideologies:
            ideologydict[each] = True
    while line:
        line = file.readline()
        if depth == 1 and '= {' in line:
            ideology = line.split(' = {')[0].strip()
            if debug is True:
                print(ideology)
            if ideology in ideologydict:
                ideologydict[ideology] = True
        if depth == 2 and 'types = {' in line:
            istypes = True
        if depth == 3 and '= {}' in line and istypes:
            ideology = line.split('= {}')[0].strip()
            if debug is True:
                print(ideology)
            if ideology in ideologydict:
                ideologydict[ideology] = True

        if '{' in line:
            depth = depth + 1
        if '}' in line:
            depth = depth - 1
        if depth == 2 and istypes:
            istypes = False
    for item in ideologydict:
        if ideologydict[item] is False:
            result = "The ideology " + item + " referenced in " + filedict[item] + " on line " + str(linedict[item]) + " is not defined"
            if debug is True:
                print(result)
            output_file.write(result)