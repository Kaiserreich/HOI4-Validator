from codecs import open

def open_file(path):
    try:
        with open(path, 'r', 'utf-8-sig') as f:
            fle = f.read()
    except Exception as inst:
        with open(path, 'r', 'ANSI') as f:
            fle = f.read()
    else:
        with open(path, 'r', 'utf-8-sig') as f:
            fle = f.read()
    return fle