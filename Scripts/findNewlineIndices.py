def find_indices_of_new_lines(contents):
    new_line_indices = []
    index = -1
    while True:
        index = contents.find('\n', index+1)
        # find returns -1 when nothing is found after the starting index
        if index != -1:
            new_line_indices += [index]
        else:
            break
    return new_line_indices