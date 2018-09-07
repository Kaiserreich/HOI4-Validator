from os import listdir
from os.path import isdir
from timedFunction import timed
from openFile import open_file
from removeComments import remove_comments


@timed
def check_endlines(path, output_file):
    check(path, output_file, "\\localisation")


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
        within_quotes = False
        current_line = 1
        for i in range(0, len(string_without_comments)):
            if string_without_comments[i] == "\"":
                within_quotes = not within_quotes
            if not within_quotes:
                if string_without_comments[i] == '\n':
                    current_line += 1
            if within_quotes:
                if string_without_comments[i:i+2] == '/n' or string_without_comments[i:i+2] == '\\N':
                    output_file.write(sub_path + '\\' + filename + ' improper newline on line ' + str(current_line) + '\n')
                if string_without_comments[i:i+2] == '\\n':
                    if string_without_comments[i - 1] == ' ':
                        output_file.write(sub_path + '\\' + filename + ' space before newline on line ' + str(current_line) + '\n')
                    if i < len(string_without_comments) - 1:
                        if string_without_comments[i + 2] == ' ':
                            output_file.write(sub_path + '\\' + filename + ' space after newline on line ' + str(current_line) + '\n')


