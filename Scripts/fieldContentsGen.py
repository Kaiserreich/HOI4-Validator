import bisect

from findNewlineIndices import find_indices_of_new_lines


def field_contents_gen(string, field_name):
    index = 0
    indices_of_newlines = find_indices_of_new_lines(string)
    while index < len(string):
        next_id_index = string.find(field_name, index)
        if next_id_index == -1:
            break
        elif string[next_id_index - 1] in ' \r\n\t':
            id_start = next_id_index + len(field_name)
            while not string[id_start].isalnum():
                id_start += 1
            id_end = id_start
            while not string[id_end] in ' \r\n\t}':
                id_end += 1
            yield string[id_start:id_end],  bisect.bisect(indices_of_newlines, id_start) + 1
            index = id_end + 1
        else:
            index = next_id_index + 1