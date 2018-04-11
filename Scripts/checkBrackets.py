from os import listdir
from os.path import isdir
import time
from openFile import open_file

def check_brackets(path, output_file):
    t0 = time.time()
    check(path, output_file, "\\events")
    check(path, output_file, "\\common")
    check(path, output_file, "\\interface")
    check(path, output_file, "\\history")
    t0 = time.time() - t0
    print("Time taken for Brackets script: " + (t0*1000).__str__() + " ms")

def check(path, output_file, sub_path):
    original_path = path
    path += sub_path
    for filename in listdir(path):
        if(isdir(path + '\\' + filename)):
            check(original_path, output_file, sub_path + '\\' + filename)
            continue
        current_line = 0
        file = open_file(path + '\\' + filename)
        line = file.readline()
        current_line += 1
        stack = []
        while line:
            for letter in line:
                if letter == '#':
                    break
                elif letter == '(':
                    stack.append(')')
                elif letter == '[':
                    stack.append(']')
                elif letter == '{':
                    stack.append('}')
                elif letter == ')' or letter == ']' or letter == '}':
                    if (len(stack) == 0):
                        output_file.write(
                            sub_path + '\\' + filename + " Brackets: Not expected '" + letter + "' around line " + str(
                                current_line) + '\n')
                    else:
                        letterPop = stack.pop()
                        if (letterPop != letter):
                            output_file.write(
                                sub_path + '\\' + filename + " Brackets: Expecting: '" + letterPop + "' but found '" + letter + "' around line " + str(
                                    current_line) + '\n')
            line = file.readline()
            current_line += 1
        if len(stack) > 0:
            output_file.write(sub_path + '\\' + filename + " Brackets: there are " + str(
                len(stack)) + " opening bracket(s) without closing bracket(s)\n")
