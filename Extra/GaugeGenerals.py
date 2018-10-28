from codecs import open
import sys
from os import listdir
import os
import time
from os import listdir
from os import walk
from os import path
from codecs import open

def print_general(generals, to_find):
    print(to_find + ":", generals[to_find])

def main():
    cpath = sys.argv[1]
    ok = 0
    for string in sys.argv:
        if ok < 2:
            ok += 1
        else:
            cpath += ' ' + string
    cpath = "C:\\Users\\Martijn\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\KRBU\\history\\countries\\"

    ttime = time.time()

    total_generals = 0
    generals = {}  # name : (G/FM, skill, A, D, P, L, SUM)
    tags = {}
    for filenames in listdir(cpath):
         with open(path.join(cpath, filenames),'r', 'utf-8-sig') as file:
            lines = file.readlines()
            current_general = ""
            searching = False
            skill = 999
            attack = 999
            defense = 999
            planning = 999
            logistics = 999
            level = 0
            sum = 999
            tag = "REEEEEEEEE"
            g_or_fm = 'REEEEEEEEEEEE'
            for x in range(0, len(lines)-1):
                line = lines[x].strip()
                if '#' in line:
                    line = line.split('#')[0].strip()
                if ('field_marshal' in line or 'corps_commander' in line) and '{' in line and level == 0:
                    if 'field_marshal' in line:
                        g_or_fm = 'FM'
                    else:
                        g_or_fm = 'G'
                    try:
                        current_general = lines[x+1].split("\"")[1]
                    except IndexError:
                        print(filenames, x+1)
                        print(lines[x+1])
                    tag = filenames[0:3]
                    tags[tag] = 0
                    total_generals += 1
                    searching = True
                    #print(current_general)
                if '=' in line and searching is True :
                    if line.split('=')[0].strip() == "skill":
                        skill = int(line.split('=')[1])
                if 'attack_skill' in line and searching is True:
                    attack = int(line.split('=')[1])
                if 'defense_skill' in line and searching is True:
                    defense = int(line.split('=')[1])
                if 'planning_skill' in line and searching is True:
                    planning = int(line.split('=')[1])
                if 'logistics_skill' in line and searching is True:
                    logistics = int(line.split('=')[1])
                if '}' in line and searching is True and level == 1 and 'trait' not in line:
                    searching = False
                    generals[current_general] = (g_or_fm, skill, attack, defense, planning, logistics, attack+defense+planning+logistics, tag)
                    #print(current_general, generals[current_general])
                if '{' in line:
                    level += line.count('{')
                if '}' in line:
                    level -= line.count('}')

    up_1 = 0
    up_2 = 0
    up_3 = 0
    up_4 = 0
    up_5 = 0
    up_6_more = 0
    perfect = 0
    op_1 = 0
    op_2 = 0
    op_3 = 0
    op_4 = 0
    op_5 = 0
    op_6_more = 0
    max_sum = 0
    max_gen = ""
    min_sum = 0
    min_gen = ""

    max_sum2 = 0
    max_sum_gen = ""
    output_file = open("generals.txt", 'w', 'utf-8-sig')

    per_level = 3
    starting = 4
    for general in generals:
        rank, skill, A, D, P, L, sum, tag = generals[general]
        target = (skill-1) * per_level + starting
        deviance = sum-target
        if abs(deviance) >2:
            output_file.write(general + ": " + str(generals[general]) + "\n")
            tags[tag] += 1
        if deviance < -5:
            up_6_more += 1
        elif deviance < -4:
            up_5 += 1
        elif deviance < -3:
            up_4 += 1
        elif deviance < -2:
            up_3 += 1
        elif deviance < -1:
            up_2 += 1
        elif deviance < 0:
            up_1 += 1
        elif deviance < 1:
            perfect += 1
        elif deviance < 2:
            op_1 += 1
        elif deviance < 3:
            op_2 += 1
        elif deviance < 4:
            op_3 += 1
        elif deviance < 5:
            op_4 += 1
        elif deviance < 6:
            op_5 += 1
        else:
            op_6_more += 1

        if deviance > max_sum:
            max_sum = deviance
            max_gen = general
        elif deviance == max_sum:
            max_gen += ", " + general

        if sum > max_sum2:
            max_sum2 = sum
            max_sum_gen = general
        elif deviance == max_sum2:
            max_sum_gen += ", " + general

        if deviance < min_sum:
            min_sum = deviance
            min_gen = general
        elif deviance == min_sum:
            min_gen += ", " + general
    max_tag_no = 0
    max_tag = ""
    for tag in tags:
        if tags[tag] > max_tag_no:
            max_tag = tag
            max_tag_no = tags[tag]
        elif tags[tag] == max_tag_no:
            max_tag += ', ' + tag
    print("Max Stat:", max_sum_gen, generals[max_sum_gen])
    print("Most OP nations:", max_tag+ ",", max_tag_no)
    print("Total Generals:", total_generals)
    print("Underpowered by 6 or more:", up_6_more)
    print("Underpowered by 5:", up_5)
    print("Underpowered by 4:", up_4)
    print("Underpowered by 3:", up_3)
    print("Underpowered by 2:", up_2)
    print("Underpowered by 1:", up_1)
    print("Perfection:", perfect)
    print("Overpowered by 1:", op_1)
    print("Overpowered by 2:", op_2)
    print("Overpowered by 3:", op_3)
    print("Overpowered by 4:", op_4)
    print("Overpowered by 5:", op_5)
    print("Overpowered by 6 or more:", op_6_more)
    print("Too OP:", op_3+op_4+op_5+op_6_more)
    print("Most OP:")
    for name in max_gen.split(','):
        print_general(generals, name.strip())
    print("Most UP:")
    for name in min_gen.split(','):
        print_general(generals, name.strip())



    print("Total Time: %.3f ms" % ((time.time() - ttime) * 1000))

if __name__ == "__main__":
    main()