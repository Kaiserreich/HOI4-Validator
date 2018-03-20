from os import listdir
from codecs import open


def kr_missing_militia_and_garrison (path, output_file):
    path += "\\common\\units\\names_divisions"
    for filename in listdir(path):
        has_garrison = 0
        has_militia = 0
        file = open(path+'\\'+filename, 'r', 'utf-8-sig')
        line = file.readline()
        while line:
            split_line = line.split(' ')
            if 'division_types' in split_line[0]:
                for string in split_line:
                    if "#" in string:
                        break
                    if "garrison" in string:
                        has_garrison += 1
                    if "militia" in string:
                        has_militia += 1
            line = file.readline()
        if has_militia == 0:
            output_file.write("\\common\\units\\names_divisions\\" + filename + " has no militia\n")
        if has_garrison == 0:
            output_file.write("\\common\\units\\names_divisions\\" +  filename + " has no garrison\n")