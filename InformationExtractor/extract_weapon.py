import re

from InformationExtractor import IO as io


def get_weapons(weapons, story):
    if len(weapons) == 0:
        weapons = io.get_weapons()

    m = re.findall(r'(' + weapons + ')', story)
    if len(m):
        val = m[0][00].strip().upper()
        return val if val != 'CAR' else val + ' BOMB'
    else:
        return '-'
