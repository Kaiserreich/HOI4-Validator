import os
from createDict import create_search_dict
from createDict import search_effects
from timedFunction import timed
from openFile import open_file

@timed
def check_ideologies(path, output_file):
    ideologypath = os.path.join(path, 'common', 'ideologies')