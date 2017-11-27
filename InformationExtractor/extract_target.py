import re


def getTarget(ne_tree):
    for i in range(0, len(ne_tree)):
        item = str(ne_tree[i]).lower()

        m = re.findall(r'(' + '\\bexploded\\b|\\battack\\b|\\battacks\\b|\\bterrorist\\b|\\battacked\\b|\\bblown\\b|'
                              '\\bfire\\b|\\bto\\b|\\bplanted\\b|\\bdetonated\\b|\\bset\\b|\\busurp\\b|\\bblew\\b'
                              '\\bintended\\b|\\bplaced\\b|\\bsabotaged\\b' + ')', item)

        if len(m) > 0:

            if m[0] == 'attack' or m[0] == 'attacks' or m[0] == 'terrorist' or m[0] == 'to' or m[0] == 'set' \
                    or m[0] == 'blew' or m[0] == 'intended' or m[0] == 'placed':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\btarget\\b|\\bbombs\\b|\\bup\\b|\\bagainst\\b|\\bon\\b|\\battack\\b|\\bthrown\\b|\\bdamage\\b|\\boff\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0:
                            return findFistOrganization(aPos + 1, ne_tree)

            # Reverse Search
            if m[0] == 'blown' or m[0] == 'fire':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\bup\\b|\\bon\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0:
                            return reverseSearch(aPos + 1, ne_tree)
            if m[0] == 'attacked' or m[0] == 'exploded' or m[0] == 'planted' or m[0] == 'detonated' or m[0] == 'usurp' or m[0] == 'sabotaged':
                return findFistOrganization(i + 1, ne_tree)

    return '-'


def reverseSearch(pos, ne_tree):
    for j in range(pos, pos - 20, -1):
        if j < 0:
            break
        val = search(j, ne_tree)
        if val != None:
            return val
    return '-'


def findFistOrganization(pos, ne_tree):
    for j in range(pos, pos + 20):
        if j >= len(ne_tree):
            break
        val = search(j, ne_tree)
        if val != None:
            return val

    val = searchNN(pos, ne_tree)
    return val if val != None else '-'

def searchNN(pos, ne_tree):
    res = ''
    while True:
        item = ne_tree[pos]
        victim = str(ne_tree[pos]).lower()

        m = re.findall(r'(' + 'tonight|today|early|tomorrow|yesterday|night|morning|afternoon|evening|monday|tuesday|wednesday|thrusday|friday'
                              '|saturday|sunday' + ')', victim)

        #if 'nn' in victim and 'tonight' not in victim and 'today' not in victim and 'friday' not in victim:

        other = re.findall(r'(' + '\'in\'|\'the\'|\'and\'' + ')', victim)

        POS = item[1] if isinstance(item, tuple) else item[0][1]

        matchPOS = re.match('\\bNN\\b', POS)

        if 'bomb' not in victim and (matchPOS != None or res != '' and (len(other) > 0)) and len(m) <= 0:

        # if 'nnp' in victim:
            if isinstance(ne_tree[pos], tuple):
                res += ne_tree[pos][0] + ' '
                pos += 1
            else:
                for t in ne_tree[pos]:
                    res += t[0] + ' '
                    pos += 1
                #return res
        else:
            break

    return None if res == '' else process(res)

def search(pos, ne_tree):

    person = False
    res = ''
    try:
        while True:
            item = ne_tree[pos]
            victim = str(ne_tree[pos]).lower()

            m = re.findall(r'(' + 'organization' + ')', victim)

            if len(m) > 0 and not isinstance(item, tuple):
                for t in item:
                    res += t[0] + ' '
                pos += 1
            else:
                break

        return process(res)
    except:
        return process(res)

def process(res):
    res = res.strip()
    res = res.replace('Destroying Windows', '')
    res.strip()
    if res.strip() != '':
        print(res.strip())
    return None if res == '' else res.strip()