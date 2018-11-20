import os
from openFile import open_file
from timedFunction import timed

@timed
def check_for_naval_aviation_tech(path, output_file):
    debug = False
    path = os.path.join(path, 'history', 'countries')
    checkarray = ['nav_av_one', 'nav_av_two', 'nav_av_three', 'carrier_one', 'carrier_two', 'carrier_three', 'heavy_carrier_one']

    for filename in os.listdir(path):
        #this creates dicts of tags that use various techs and sees if they have the prereqs for them
        if ".txt" in filename:
            array= [False, False, False, False, False, False, False]
            file = open_file(os.path.join(path, filename))
            line = file.readline()
            while line:
                i = 0
                while i < len(checkarray):
                    if checkarray[i] in line:
                        array[i] = True
                    i = i +1
                line = file.readline()
            if array[0] == False and (array[3] == True or array[4] == True or array[5] == True or array[6] == True):
                result = filename + ' does not have nav_av_one but does have some form of naval aviation.\n'
                if debug == True:
                    print(result)
                output_file.write(result)
            elif array[1] == False and (array[4] == True or array[5] == True or array[6] == True):
                result = filename + ' does not have nav_av_two but does have carrier 2 or higher, or heavy carriers\n'
                if debug == True:
                    print(result)
                output_file.write(result)
            elif array[2] == False and (array[5] == True or array[6] == True):
                result = filename + ' does not have nav_av_three but does have carrier 3 or higher, or heavy carriers\n'
                if debug == True:
                    print(result)
                output_file.write(result)