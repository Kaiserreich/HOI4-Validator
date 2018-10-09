import bisect

from changeInScopeLevel import change_in_scope_level
from findNewlineIndices import find_indices_of_new_lines


def scope_gen(string, search_terms):

    def find_end_index(string, start_index):
        potential_end_index = start_index + 1
        scope_level = 1
        while scope_level != 0:
            potential_end_index += 1
            character = string[potential_end_index]
            scope_level += change_in_scope_level(character)
        return potential_end_index

    def not_within_word(string, index):
        if index == 0:
            return True
        else:
            return string[index-1] in ' \n\t'

    indices_of_newlines = find_indices_of_new_lines(string)
    index = -1
    while True:
        index = find_next_occurance_of_terms(index, search_terms, string)
        # find returns -1 when nothing is found after the starting index
        if index != -1 and not_within_word(string, index):
            try:
                while string[index] != '{':
                    index += 1
            except IndexError:
                break
            start_index = index
            # if there is a bracket mismatch, just end the generator
            try:
                end_index = find_end_index(string, start_index)
            except IndexError:
                break
            event_body = string[start_index:end_index + 1]
            # +1 since lines start at 1
            start_line = bisect.bisect(indices_of_newlines, start_index) + 1
            yield event_body, start_line
            index = end_index
        else:
            break


def find_next_occurance_of_terms(index, search_terms, string):
    non_zero_search_terms = []
    for search_term in search_terms:
        next_index = string.find(search_term, index + 1)
        if next_index >= 0:
            non_zero_search_terms += [search_term]
    if len(non_zero_search_terms) == 0:
        return -1
    else:
        minimun = min([string.find(search_term, index + 1) for search_term in non_zero_search_terms])
        return minimun