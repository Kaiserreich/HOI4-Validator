import os
from openFile import open_file
from timedFunction import timed

@timed
def check_for_naval_aviation_tech(path, output_file):
    debug = False
    path = os.path.join(path, 'history', 'countries')

    for filename in os.listdir(path):
        #this creates dicts of tags that use various techs and sees if they have the prereqs for them
        if ".txt" in filename:
            #this is the most bullshit name for a dictionary ever, but in my defense, fuck you
            array = {     'nav_av_one': False,
                          'nav_av_two': False,
                          'nav_av_three':False,
                          'nav_infra_one': False,
                          'nav_infra_two': False,
                          'nav_infra_three': False,
                          'carrier_one':False,
                          'carrier_two':False,
                          'carrier_three':False,
                          'heavy_carrier_one':False,
                          'heavy_cruiser_one': False,
                          'heavy_cruiser_three': False,
                          'heavy_cruiser_five': False,
                          'dreadnought_one': False,
                          'dreadnought_four': False,
                          'battleship_four': False
                          }
            file = open_file(os.path.join(path, filename))
            line = file.readline()
            while line:
                for key in array:
                    if key in line:
                        array[key] = True
                line = file.readline()
            result = ""
            navavresult = True
            if array['nav_av_one'] is False and (array['carrier_one'] == True or array['carrier_two'] or array['carrier_three'] or array['heavy_carrier_one']):
                result = filename + ' does not have nav_av_one but does have some form of naval aviation.\n'
            elif array['nav_av_two'] is False and (array['carrier_two'] or array['carrier_three'] or array['heavy_carrier_one']):
                result = filename + ' does not have nav_av_two but does have carrier 2 or higher, or heavy carriers\n'
            elif array['nav_av_three'] is False and (array['carrier_three'] or array['heavy_carrier_one']):
                result = filename + ' does not have nav_av_three but does have carrier 3 or higher, or heavy carriers\n'
            else:
                navavresult = False
            if navavresult:
                if debug:
                    print(result)
                output_file.write(result)

            infresult = True
            if array['nav_infra_one'] is False and (array['carrier_two'] or array['carrier_three'] or array['heavy_carrier_one'] or array['heavy_cruiser_one'] or
                                                    array['heavy_cruiser_three'] or array['heavy_cruiser_five'] or array['dreadnought_one'] or array['dreadnought_four'] or array['battleship_four']):
                result = filename + ' does not have nav_infra_one but does have naval tech that requires it.\n'
            elif array['nav_infra_two'] is False and (array['carrier_three'] or array['heavy_carrier_one'] or
                                                    array['heavy_cruiser_three'] or array['heavy_cruiser_five'] or array['dreadnought_one'] or array['dreadnought_four'] or array['battleship_four']):
                result = filename + ' does not have nav_infra_two but does have naval tech that requires it.\n'
            elif array['nav_infra_three'] is False and (array['heavy_carrier_one'] or array['heavy_cruiser_five'] or array['dreadnought_four'] or array['battleship_four']):
                result = filename + ' does not have nav_infra_three but does have naval tech that requires it.\n'
            else:
                infresult = False
            if infresult:
                if debug:
                    print(result)
                output_file.write(result)
