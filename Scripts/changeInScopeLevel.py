def change_in_scope_level(char):
    if char == '{':
        return 1
    elif char == '}':
        return -1
    else:
        return 0