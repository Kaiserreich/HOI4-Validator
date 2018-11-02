from timedFunction import timed
from usefulNamedTuples import Bug
from stringAndFileFromPath import files_as_strings_from_path_gen
import os

@timed
def check_endlines(path, output_file):

    def check_newlines_in_string(filename, string):
        within_quotes = False
        current_line = 1
        for i in range(0, len(string)):
            if string[i] == "\"":
                within_quotes = not within_quotes
            if not within_quotes:
                if string[i] == '\n':
                    current_line += 1
            if within_quotes:
                if string[i:i + 2] == '/n' or string[i:i + 2] == '\\N':
                    yield Bug('Improper newline', current_line, filename)
                if string[i:i + 2] == '\\n':
                    if string[i - 1] == ' ':
                        yield Bug('Space before newline', current_line, filename)
                    if i < len(string) - 1:
                        if string[i + 2] == ' ':
                            yield Bug('Space after newline', current_line, filename)

    bugs = []
    path = os.path.join(path,"localisation")
    for string, filename in files_as_strings_from_path_gen(path):
        bugs += [bug for bug in check_newlines_in_string(filename, string)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')
