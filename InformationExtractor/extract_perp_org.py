import re

def get_perp_org(ne_tree):

    for i in range(0, len(ne_tree)):
        item = str(ne_tree[i]).lower()

        m = re.findall(r'(' + '\\bsuspect\\b|\\bsuspects\\b|\\blaunched\\b|\\bintercepted\\b|\\bclaimed\\b'
                              '|\\bkidnapping\\b|\\barrest\\b|\\bplanted\\b|\\bshot\\b'
                              '|\\bincident\\b|\\bkilled\\b|\\bmurderers\\b' + ')', item)

        if 'arrest' in item:
            print()
        if len(m) > 0:

            if m[0] == 'launched' or m[0] == 'intercepted' or m[0] == 'kidnapping' or m[0] == 'arrest' \
                    or m[0] == 'planted' or m[0] == 'shot' or m[0] == 'incident' :
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\bby\\b|\\bof\\b|\\bagainst\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0:
                            if not isinstance(item, tuple):
                                return findFistOrganization(aPos, ne_tree)
                            return findFistOrganization(aPos+1, ne_tree)

            # Reverse Search
            if m[0] == 'claimed' or m[0] == 'killed'or m[0] == 'murderers':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\bresponsibility\\b|\\bof\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0 or m[0] == 'killed':
                            return reverseSearch(aPos - 1, ne_tree)
            if m[0] == 'arrest':
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
    res = ''
    while True:
        item = ne_tree[pos]
        victim = str(ne_tree[pos]).lower()

        m = re.findall(r'(' + '\(organization|\(person|\(facility|\(gsp' + ')', victim)
        #m = re.findall(r'(' + 'nnp' + ')', victim)

        # if 'NNP' in victim:
        if len(m) > 0:
            for t in item:
                res += t[0] + ' '
            pos += 1
        else:
            break

    res = res.replace('Arrest Of', '')
    res = res.replace('Msgr', '')

    if res.strip() != '':
        print(res.strip())
    return None if res.strip() == '' else res.strip()

