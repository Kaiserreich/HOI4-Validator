import os
from openFile import open_file
from timedFunction import timed

@timed
def check_OOB_Contents(path, output_file, optionsdict):
    checktemplate = optionsdict["check_oob_templates"]
    checknamegroup = optionsdict["check_template_namegroup"]
    checknames = optionsdict["check_template_names"]
    checkafter = optionsdict["check_OOB_order"]
    path = os.path.join(path, 'history', 'units')
    afterset = set()
    checktemplateresult = ""
    checknamegroupresult = ""
    checknamesresult = ""
    debug = False
    for filename in os.listdir(path):
        if 'unlock' in filename:
            continue
        if debug:
            print("looking at " + filename)
        forgotname = set()
        file = open_file(os.path.join(path, filename))
        line = file.readline()
        templatenamegroup = set()
        calledtemplates = {}
        templatenames = {}
        inunits = False
        innavy = False
        lineno = 1;
        templateno = 0;
        name = ""
        depth = 0
        while line:
            if '{' in line:
                depth = depth +1
            if '}' in line:
                depth = depth - 1
            if inunits == False and innavy == False:
                if 'units = {' in line:
                    inunits = True
                if 'navy = {' in line:
                    innavy = True
                if 'division_template = {' in line:
                    name = ""
                    templateno = templateno + 1
                    forgotname.add(templateno)
                    templatenamegroup.add(templateno)
                if 'name = ' in line:
                    if debug and filename == "OMA.txt":
                        print(line)
                    name = ' '.join(line.split()).split('name = "')[1].split("\"")[0].strip()
                    templatenames[templateno] = name
                    forgotname.remove(templateno)
                if 'division_names_group' in line and checknamegroup:
                    templatenamegroup.remove(templateno)
            elif inunits:
                if 'division_template = ' in line:
                    if '{' not in line:
                        if checktemplate:
                            name = ' '.join(line.split()).split('division_template = "')[1].split("\"")[0].strip()
                            if (name in templatenames.values()) is False and checktemplate is True:
                                calledtemplates[name] = filename
                    elif checkafter == True:
                        afterset.add(filename)
            else:
                if depth == 0:
                    innavy = False
            lineno = lineno+1;
            line = file.readline()
        if checktemplate:
            for item in calledtemplates:
                checktemplateresult = checktemplateresult + "The division template " + item +" called in file " + calledtemplates[item] + " does not exist.\n"
        if checknamegroup:
            for item in templatenamegroup:
                checknamegroupresult = checknamegroupresult + templatenames[item].replace("\"", "") + " the " + number(item) +" division template in " + filename +" has no namegroup \n"
        if checknames:
            for item in forgotname:
                checknamesresult = checknamesresult + "The " + number(item) + "rd template in file " + filename + "has no name"
        if debug:
            print(templatenames.values())
    if checktemplate:
        if debug:
            print(checktemplateresult)
        output_file.write(checktemplateresult)
    if checknamegroup:
        if debug:
            print(checknamegroupresult)
        output_file.write(checknamegroupresult)
    if checknames:
        if debug:
            print(checknamesresult)
        output_file.write(checknamesresult)
    if checkafter:
        for item in afterset:
            result = "File " + item + " has division templates defined after the unit definitions.\n"
            if debug:
                print(result)
            output_file.write(result)

def number(number):
    if number == 1:
        return "1st"
    elif number == 2:
        return "2nd"
    elif number == 3:
        return "3rd"
    else:
        return str(number) + "th"
