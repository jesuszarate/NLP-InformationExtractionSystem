import re

def get_victim(ne_tree):

    for i in range(0, len(ne_tree)):
        item = str(ne_tree[i]).lower()

        m = re.findall(r'(' + '\\battack\\b|\\battempt\\b|\\bassassination\\b|\\bwounded\\b|\\bkidnapped\\b|\\bvictims\\b'
                              '|\\bmurdered\\b|\\bmurderers\\b|\\bmurder\\b|\\bmassacre\\b|\\bmassacred\\b|\\bkilled\\b|'
                              '\\bdeath\\b|\\bshot\\b|\\bwere\\b|\\bwas\\b|\\bdisappearance\\b' + ')', item)

        if len(m) > 0:

            if m[0] == 'attack' or m[0] == 'attempt' or m[0] == 'victims' or m[0] == 'wounded' or m[0] == 'life' or \
                            m[0] == 'assassination' or m[0] == 'were' or m[0] == 'massacre' or \
                            m[0] == 'murder' or m[0] == 'death'or m[0] == 'disappearance':

                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\binclude\\|\\bon\\b|\\bagainst\\b|\\bby\\b|\\bof\\b|\\binjured\\b|\\bare\\b|\\bidentified\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0 or 'include' in item:
                            if m[0] == 'murder':
                                return findFistOrganization(aPos, ne_tree)
                            return findFistOrganization(aPos + 1, ne_tree)

            # Reverse Search
            if m[0] == 'claimed' or m[0] == 'kidnapped' or m[0] == 'shot' or m[0] == 'were' or m[0] == 'was' or m[0] == 'killed':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\bkilled\\b|\\bresponsibility\\b|\\bby\\b|\\bwounded\\b|\\bin\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0 or m[0] == 'kidnapped' or 'shot':
                            return reverseSearch(aPos - 1, ne_tree)
            if m[0] == 'murdered':
                return findFistOrganization(i + 1, ne_tree)

    return '-'


def reverseSearch(pos, ne_tree):
    person = False
    val = ''
    for j in range(pos, pos - 10, -1):
        if j < 0:
            break
        person, val = search(j, ne_tree)
        if val != None:# and person:
            return val
    # nnp = findNNP(pos, ne_tree)
    #
    # return '-' if nnp == None else nnp.strip()
    return '-' if val == None else val


def findNNP(pos, ne_tree):
    person = False
    val = ''
    for j in range(pos, pos - 10, -1):
        if j < 0:
            break
        # person, val = search(j, ne_tree)
        victim = str(ne_tree[j]).lower()
        if 'nnp' in victim:
            if isinstance(ne_tree[j], tuple):
                return ne_tree[j][0]
            else:
                for t in ne_tree[j]:
                    val += t[0] + ' '
                return val

    return '-' if val == None else val


def findFistOrganization(pos, ne_tree):
    person = False
    val = ''
    for j in range(pos, pos + 10):
        if j >= len(ne_tree):
            break
        person, val = search(j, ne_tree)
        if val != None:# and person:
            return val
    return '-' if val == None else val

def search(pos, ne_tree):

    person = False
    res = ''
    try:
        while True:
            item = ne_tree[pos]
            victim = str(ne_tree[pos]).lower()

            if 'jesuits' in victim:
                return True, 'Jesuits'

            if 'person' in victim:
                person = True

            m = re.findall(r'(' + 'person|organization' + ')', victim)
            # m = re.findall(r'(' + 'person' + ')', victim)

            if m[0] == 'person' and isinstance(item, tuple):
                return True, 'Persons'

            if len(m) > 0 and not isinstance(item, tuple):
                for t in item:
                    res += t[0] + ' '
                pos += 1
            else:
                break

        return person, process(res)
    except:
        return person, process(res)

def process(res):
    res = res.strip()
    res = res.replace('Murder Of', '')
    res = res.replace('Was Shot', '')
    res = res.replace('Burial Of The 10', '')
    res = res.replace('Recent Disgraceful', '')
    res = res.replace('Has', '')
    res.strip()
    # if res.strip() != '':
    #     print(res.strip())
    return None if res == '' else res.strip()