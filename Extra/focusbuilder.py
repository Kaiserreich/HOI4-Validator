from codecs import open
import sys




def main():
    file_paths = sys.argv[1:]
    filenames = []
    for p in file_paths:
        filenames.append(p)

    for filename in filenames:
        if ".txt" in filename:
            counter = 0
            temp_string = filename.split('\\')[len(filename.split('\\')) - 1].split('.')[0]
            print("Working on " + temp_string)
            temp_string = temp_string + ".yml"
            output_file = open(temp_string, 'w', 'utf-8-sig')
            output_file.write("l_english: \n\n")

            file = open(filename, 'r', 'ansi')
            lines = file.readlines()
            for string in lines:
                if "id " in string and string.strip().startswith('#') is False and 'relative_position_id' not in string:
                    if counter != 0:
                        focus = string.split('=')[1].strip()
                        output_file.write(" " + focus + ":0 \"\"\n")
                        output_file.write(" " + focus + "_desc:0 \"\"\n")
                    counter += 1
        else:
            temp_string = filename.split('\\')[len(filename.split('\\')) - 1]
            print("Error: " + temp_string + " is not a focus file")

    input('Press enter to continue: ')


if __name__ == "__main__":
    main()