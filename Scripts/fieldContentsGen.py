import bisect
import re

from findNewlineIndices import find_indices_of_new_lines
from changeInScopeLevel import change_in_scope_level


def field_contents_gen(string, field_name):
    index = 0
    indices_of_newlines = find_indices_of_new_lines(string)
    while index < len(string):
        next_id_index = string.find(field_name, index)
        if next_id_index == -1:
            break
        elif string[next_id_index - 1] in ' \r\n\t' and string[next_id_index+len(field_name)] in ' \r\n\t=':
            id_start = next_id_index + len(field_name)
            while string[id_start] in ' \r\n\t=':
                id_start += 1
            if string[id_start] == '{':
                id_end = id_start + 1
                scope_level = 1
                try:
                    while scope_level != 0:
                        scope_level += change_in_scope_level(string[id_end])
                        id_end += 1
                    for item in parse_list(string[id_start:id_end]):
                        yield item, bisect.bisect(indices_of_newlines, id_start) + 1
                except IndexError:
                    pass
            else:
                id_end = id_start
                while not string[id_end] in ' \r\n\t}':
                    id_end += 1
                yield string[id_start:id_end],  bisect.bisect(indices_of_newlines, id_start) + 1
            index = id_end + 1
        else:
            index = next_id_index + 1


def parse_list(string):
    stripped = string.strip(' \n\t\r{}')
    list = re.split(r'\W+', stripped)
    return filter(None, list)