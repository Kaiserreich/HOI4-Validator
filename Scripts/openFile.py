from codecs import open

def open_file(path):
    file = open(path, 'r', 'utf-8-sig')
    try:
        file.read()
    except Exception as inst:
        file = open(path, 'r', 'ANSI')
    else:
        file = open(path, 'r', 'utf-8-sig')
    return file