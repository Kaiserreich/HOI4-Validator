from codecs import open
from os import listdir
from os import path



def main():
    mod_path = r'C:\Users\Martijn\Documents\Paradox Interactive\Hearts of Iron IV\mod\KROTHER'
    tech_folder = path.join(mod_path, 'common', 'technologies')
    scripted_effects = path.join(mod_path, 'common', 'scripted_effects')

    template = "\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tPREV = {\n\t\t\t\t\thas_tech = %(tech)s\n\t\t\t\t}\n\t\t\t}\n\t\t\tset_technology = {\n\t\t\t\t%(tech)s = 1\n\t\t\t}\n\t\t}\n"

    with open(path.join(scripted_effects, 'transfer_technology_effects_new.txt'), 'w', 'utf-8') as new_scripted_effect:
        # Its ugly, but works
        intro_string = """### Transfer Technology
### Written by wyandotte
### Automated by Dr_Njitram
#
# How to use:
#
#	TAG = {
#		transfer_technology = yes
#	}
#
# As it uses 'PREV', you need to make sure the previous TAG is the one you transfer from
# And the TAG you transfer *to* is the scope in which the effect is called.
#
# For example, an event fires for FOO. That country wants to transfer techs to BAR
# In an event option:
#
# BAR = {
#	transfer_technology = yes
#
transfer_technology = {
\thidden_effect = {
"""

        new_scripted_effect.write(intro_string)
        for filename in listdir(tech_folder):
            new_scripted_effect.write('\t\t###' + filename[:-4] + '###\n')
            with open(path.join(tech_folder, filename), 'r', 'utf-8') as file:
                lines = file.readlines()
                level = 0

                for line_number, line in enumerate(lines):
                    if '#' in line:
                        if line.strip().startswith("#") is True:
                            continue
                        else:
                            line = line.split('#')[0]

                    if level == 1 and '{' in line:
                        techname = line.split('=')[0].strip()
                        new_scripted_effect.write(template % {"tech": techname})
                    if '{' in line:
                        level += line.count('{')
                    if '}' in line:
                        level -= line.count('}')

        new_scripted_effect.write("\t}\n}")


main()
