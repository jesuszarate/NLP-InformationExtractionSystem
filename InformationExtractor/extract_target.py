import re


def getTarget(ne_tree):
    for i in range(0, len(ne_tree)):
        item = str(ne_tree[i]).lower()

        m = re.findall(r'(' + '\\bexploded\\b|\\battack\\b|\\bterrorist\\b|\\bbomb\\b|\\battacked\\b|\\bblown\\b|'
                              '\\bfire\\b|\\bto\\b' + ')', item)

        if len(m) > 0:

            if m[0] == 'attack' or m[0] == 'terrorist' or m[0] == 'bomb' or m[0] == 'to':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m = re.findall(r'(' + '\\bagainst\\b|\\bon\\b|\\battack\\b|\\bthrown\\b|\\bdamage\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m) > 0:
                            return findFistOrganization(aPos + 1, ne_tree)

            # Reverse Search
            elif m[0] == 'blown' or m[0] == 'fire':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m = re.findall(r'(' + '\\bup\\b|\\bon\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m) > 0:
                            return reverseSearch(aPos + 1, ne_tree)
            else:
                return findFistOrganization(i + 1, ne_tree)

    return '-'


def reverseSearch(pos, ne_tree):
    for j in range(pos, pos - 10, -1):
        if j < 0:
            break
        val = search(j, ne_tree)
        if val != None:
            return val
    return '-'


def findFistOrganization(pos, ne_tree):
    for j in range(pos, pos + 10):
        if j >= len(ne_tree):
            break
        val = search(j, ne_tree)
        if val != None:
            return val
    return '-'

def search(pos, ne_tree):
    item = ne_tree[pos]
    victim = str(ne_tree[pos]).lower()

    m = re.findall(r'(' + 'organization|person|facility|gsp' + ')', victim)

    if len(m) > 0:
        res = ''
        for t in item:
            res += t[0] + ' '

        print(res[:-1])
        return res[:-1]
