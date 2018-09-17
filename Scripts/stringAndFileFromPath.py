import os

from openFile import open_file
from removeComments import remove_comments


def files_as_strings_from_path_gen(path):
    for directory, subdirs, files in os.walk(path):
        for file in files:
            current_file = open_file(directory + '/' + file)
            contents = current_file.read()
            contents = remove_comments(contents)
            yield contents, file