from os import listdir
from os import path
from codecs import open
import re


def check_for_missing_gfx(file_path, output_file):
    print("Just checking")
    # C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KRBU
    # this is going to be a mess

    interface_path = file_path + "\\interface"
    tags_path = file_path = "\\common\\country_tags"

    tree_path = file_path + "\\common\\national_focus"
    tree_gfx_path = file_path + "\\gfx\\interface\\goals"

    event_gfx_path  = file_path + "\\events"
    event_gfx_path = file_path + "\\gfx\\event_pictures"


    ideas_gfx_path = file_path + "\\gfx\\interface\\ideas"
    ideas_gfx_path = file_path + "\\common\\ideas" #also for ministers

    ministers_gfx_path = file_path + "\\gfx\\interface\\ministers"

    tech_gfx_path = file_path + "\\gfx\\interface\\technologies"

    leaders_gfx_path = file_path + "\\gfx\\leaders"
    country_history_path = file_path + "\\history\\countries"

    flags_gfx_path = file_path + "\\gfx\\flags"

    #Ill also need common\scripted_effects for cosmetic tags
    #fucking flags and their cosmetic tags
    #test