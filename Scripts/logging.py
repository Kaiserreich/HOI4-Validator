from pprint import PrettyPrinter
OUTPUT_FILE = open("validator.txt", 'w', -1, 'utf-8-sig')
PRETTY_PRINTER = PrettyPrinter(indent=4)

def log(message, to_file=True, output_file=OUTPUT_FILE):
    if isinstance(message, list) or isinstance(message, set) or isinstance(message, dict):
        message = PRETTY_PRINTER.pformat(message)
    else:
        message = str(message)
    print(message)
    if to_file:
        output_file.write(message + "\n")