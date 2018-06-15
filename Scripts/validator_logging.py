from pprint import PrettyPrinter
from enum import Enum
import os
import pathos

class LogLevel(Enum):
    '''CTD - will cause a CTD
    Error - will show up in error log
    Warn - may, but does not have to cause problems
    Info - none of the above
    Debug - debug only'''
    CTD = 0
    Error = 1
    Warn = 2
    Info = 3
    Debug = 4

class Logger():
    OUTPUT_FILE = "validator.txt"
    PRETTY_PRINTER = PrettyPrinter(indent=4)

    def __init__(self, output_file=OUTPUT_FILE):
        self.lock = pathos.helpers.mp.Lock()
        with open(output_file, "w") as f:
            f.write("")

    def log(self, message, level=4, script_name=os.path.basename(__file__), to_file=True, output_file=OUTPUT_FILE):
        if isinstance(message, list) or isinstance(message, set) or isinstance(message, dict):
            message = self.PRETTY_PRINTER.pformat(message)
        else:
            message = str(message)
        cpname = pathos.helpers.mp.current_process().name
        message = "[%s][%s][%s] %s" % (LogLevel(level).name, cpname, script_name, message)
        print(message)
        if to_file:
            self.lock.acquire()
            with open(output_file, "a") as f:
                f.write(message + "\n")
            self.lock.release()

LOGGER = Logger()