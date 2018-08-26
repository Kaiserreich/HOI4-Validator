def remove_comments(string):
    lines = string.split('\n')[0:-1]
    string_without_comments = ''
    for line in lines:
        line_without_comments = line.split('#')[0]
        if not line_without_comments.endswith('\n'):
            line_without_comments += '\n'
        string_without_comments += line_without_comments
    return string_without_comments