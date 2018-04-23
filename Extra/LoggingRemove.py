from codecs import open
import sys
from os import listdir


def focus(cpath):
    #immediate = {log = "Focus id: "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\common\\national_focus"):
        if ".txt" in filename and "KR" in filename:
            linenumber = 0
            outputfile = open(cpath + "\\common\\national_focus\\" + filename, 'r', 'utf-8')
            lines = outputfile.readlines()
            outputfile.close()
            outputfile = open(cpath + "\\common\\national_focus\\" + filename, 'w', 'utf-8')
            outputfile.truncate()
            for line in lines:
                linenumber += 1
                if 'log = "[GetDateText]' not in line:
                    outputfile.write(line)
                else:
                    outputfile.write("")

def event(cpath):
    # immediate = {log = "[Root.GetName]: event "+ id + "\n"}  # autolog
    for filename in listdir(cpath + "\\events"):
        if ".txt" in filename and "KR" in filename:
            outputfile = open(cpath + "\\events\\" + filename, 'r', 'utf-8-sig')
            lines = outputfile.readlines()
            outputfile.close()
            outputfile = open(cpath + "\\events\\" + filename, 'w', 'utf-8-sig')
            outputfile.truncate()
            for line in lines:
                if 'immediate = {log = ' not in line:
                    outputfile.write(line)
                else:
                    outputfile.write("")



def main():
    cpath = sys.argv[1]
    #cpath = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRBU"

    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string
    event(cpath)
    focus(cpath)


if __name__ == "__main__":
    main()

