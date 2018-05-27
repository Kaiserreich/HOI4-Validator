from codecs import open
import sys
from os import listdir
import time
import os





def main():
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string
    annex_event_file = open(cpath + "\\events\\KR_Annexations.txt", "r", "utf-8-sig")
    annex_on_action_file = open(cpath + "\\common\\on_actions\\KR_on_actions_annexations.txt", "r", "utf-8")

    dec_path = cpath + "\\common\\decisions\\"
    dec_file = open(dec_path + "KR_Annexation_decisions.txt", "w", "ansi")
    #category is KR_Annexations


if __name__ == "__main__":
    main()
