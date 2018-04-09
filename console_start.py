import os
import sys
import start

# Creating the path for the Mod

ok = 0
cpath = sys.argv[1]

for string in sys.argv:
    if ok < 2:
        ok += 1
    else:
        cpath += ' ' + string

path = cpath.split("--")[1].strip()
hoi4_path = cpath.split("--")[2].strip()

start.start(path, hoi4_path)


print ('The validator finished')
