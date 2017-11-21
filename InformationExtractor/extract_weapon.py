import re
from InformationExtractor import IO as io

def get_weapons(weapons, story):

    if len(weapons) == 0:
        weapons = io.getWeapons()

    m = re.findall(r'(' + weapons +')', story)
    if len(m):
        # print(m[0])
        return m[0].strip().upper()
    else:
        return '-'