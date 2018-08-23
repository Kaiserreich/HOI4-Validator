from os import listdir
from openFile import open_file
from timedFunction import timed


@timed
def check_for_missing_cores(path, output_file):
    path+="\\history\\states"
    filelist = []
    for filename in listdir(path):
        #this loops through all the states
        hascore = False
        current_line = 0
        file = open_file(path + '\\' + filename)
        line = file.readline()
        current_line += 1
        while line:
            if ('add_core_of = ' in line):
                #this means there is a core in the state
                hascore = True
            line = file.readline()
            current_line += 1
        if hascore ==  False:
            #all states without cores are added to the list
            filelist.append(filename)
    i = 0
    while (i < len(filelist)):
        result = "The state in " + filelist[i] + " does not have any cores\n"
        print(result)
        output_file.write(result)
        i += 1
