
import os
from createDict import create_search_dict
from createDict import search_effects
from timedFunction import timed

@timed
def check_for_vp_loc(path, output_file, endo):
    debug = False
    vpdict = {}
    locdict = {}
    linedict = {}
    filedict = {}
    loclinedict = {}
    locfiledict = {}
    searchstrings = ['victory_points = ']
    if endo:
        locsearchstrings = ['endo_vp_']
    else:
        locsearchstrings = ['VICTORY_POINTS_']
    filterstrings = []
    locfilterstrings = ['TOOLTIP']
    thingstripped = 'vp'
    locthingstripped = 'vp_loc'
    statepath = os.path.join(path, 'history', 'states')
    locpath = os.path.join(path, 'localisation')
    if debug == True:
        print("calling create search dict")
    vpdict, linedict, filedict = create_search_dict(vpdict, linedict, filedict, statepath, searchstrings, filterstrings, thingstripped)
    if debug == True:
        print("calling create search dict again")
    locdict, loclinedict, locfiledict = create_search_dict(locdict, loclinedict, locfiledict, locpath, locsearchstrings, locfilterstrings, locthingstripped, checkfiles = "victory_points")
    if locdict == {}:
        locdict, loclinedict, locfiledict = create_search_dict(locdict, loclinedict, locfiledict, locpath, locsearchstrings, locfilterstrings, locthingstripped)
    for key in locdict:
        if key in vpdict:
            vpdict[key] = True
    for key in vpdict:
        if vpdict[key] == False:
            if endo:
                result = "The vp " + key + " on line " + str(linedict[key]) + " of "+ filedict[key] + " does not have any endonym localization.\n"
            else:
                result = "The vp " + key + " on line " + str(linedict[key]) + " of "+ filedict[key] + " does not have any localization.\n"
            if debug == True:
                print(result)
            output_file.write(result)
        else:
            locdict[key] = True
    for key in locdict:
        if locdict[key] == False:
            result = "The vp localization " + key + " on line " + str(loclinedict[key]) + " of "+ locfiledict[key] + " does not have any corresponding victory point.\n"
            if debug == True:
                print(result)
            output_file.write(result)


