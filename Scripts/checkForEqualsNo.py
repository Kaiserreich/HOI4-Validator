from createDict import search_effects
from timedFunction import timed

@timed
def check_for_equals_no(path, output_file):
    #this currently searches in the wrong places because I don't know where to search. Someone tell me where to search.
    originalpath = path
    #this creates a dict of all the generals that are referenced
    nodict = {}
    linedict = {}
    filedict = {}
    searchstrings = ['= no']
    filterstrings = []
    thingstripped = '=no'
    nodict, linedict, filedict =search_effects(nodict, linedict, filedict, originalpath, searchstrings, filterstrings, thingstripped)
    #create_general_list(originalpath, output_file)
    for key in nodict:
        result = "= no is used in file " + filedict[key] + " on line " + str(linedict[key]) + ". Don't do that.\n"
        #print(result)
        output_file.write(result)
