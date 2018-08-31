import bisect
from os import listdir
from os.path import isdir
from timedFunction import timed
from openFile import open_file
from removeComments import remove_comments
from findNewlineIndices import find_indices_of_new_lines


@timed
def check_endlines(path, output_file):
    check(path, output_file, "\\events")
    check(path, output_file, "\\common")
    check(path, output_file, "\\history")


def check(path, output_file, sub_path):
    original_path = path
    path += sub_path
    for filename in listdir(path):
        if isdir(path + '\\' + filename):
            check(original_path, output_file, sub_path + '\\' + filename)
            continue
        file = open_file(path + '\\' + filename)
        string = file.read()
        string_without_comments = remove_comments(string)
        indices_of_newlines_without_comments = find_indices_of_new_lines(string_without_comments)
        for i in range(0, len(string_without_comments)):
            if string_without_comments[i:i+2] == '/n' or string_without_comments[i:i+2] == '\\N':
                line = bisect.bisect(indices_of_newlines_without_comments, i) + 1
                output_file.write(sub_path + '\\' + filename + ' improper newline on line ' + str(line) + '\n')

        indices_of_newlines = find_indices_of_new_lines(string)
        for current_line, index in enumerate(indices_of_newlines):
            if string[index - 1] == ' ':
                output_file.write(sub_path + '\\' + filename + ' space before newline on line ' + str(current_line+1) + '\n')
            if index < len(string) - 2:
                if string[index + 1] == ' ' and string[index + 2] != ' ':
                    output_file.write(sub_path + '\\' + filename + ' space after newline on line ' + str(current_line+1) + '\n')


