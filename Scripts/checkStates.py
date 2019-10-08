import os
from openFile import open_file
from createDict import search_effects
from timedFunction import timed

@timed
def check_states(path, output_file):
    originalpath = path
    #this creates a dict of all the oobs that exist
    statedict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['add_state_claim = ', 'owns_state = ', 'controls_state = ', 'transfer_state = ', 'add_state_core = ', 'state = ']
    filterstrings = []
    thingstripped = 'states'
    statedict, linedict, filedict =search_effects(statedict, linedict, filedict, originalpath, searchstrings, filterstrings, thingstripped)
    finaldict = create_state_dict(originalpath, statedict, output_file)
    for key in finaldict:
        if finaldict[key] == False:
            result = "State " + key + " referenced in " + filedict[key] + " on line " + str(linedict[key]) + " does not exist.\n"
            #print(result)
            output_file.write(result)

def create_state_dict(path, statedict, output_file):
    returndict = statedict
    path = os.path.join(path, 'history', 'states')
    for filename in os.listdir(path):
        idname = True
        try:
            fileid = int(filename.split("-")[0])
        except:
            idname = False
        file = open_file(os.path.join(path, filename))
        line = file.readline()
        while line:
            if ('id = ') in line:
                try:
                    id = int(line.split(' = ')[1].strip().split(" ")[0])
                except:
                    id = int(line.split(' = ')[1].strip())
                break
            line = file.readline()
        if idname:
            if id != fileid:
                result = "In " + filename + " the state id is " + str(id) + " instead of " + str(fileid) + ".\n"
                #print(result)
                output_file.write(result)
        returndict[str(id)] = True
    return returndict