# import nltk
# import re
# from InformationExtractor import Patterns as pat
# from nltk.chunk import conlltags2tree, tree2conlltags
#
# def find_muder_victim(ne_tree):
#     for item in ne_tree:
#         person = '\(PERSON\s.+\)'
#         organization = '\(ORGANIZATION\s.+\)'
#         entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
#         if entitiesperson != None:
#             itemStr = str(item).lower()
#
#             m = re.findall(r'(' + 'murder' + ')', itemStr)
#             #m = re.findall(r'(' + '\\bmurder\\b' + ')', itemStr)
#             if len(m) > 0:
#                 return item
#             # m = re.findall(r'(' + 'were injured' + ')', itemStr)
#
#             # if len(m) > 0:
#             #     return item
#
# def get_victims_reg(items):
#     res = ''
#     for v in items:
#         res += '{0}|'.format(v)
#     return res[:-1]
#
#
# def getEntities(ne_tree):
#
#     found_murder = False
#     #for ne in ne_tree:
#     for i in range(0, len(ne_tree)):
#         ne = ne_tree[i]
#         item = str(ne).lower()
#         m = re.findall(r'(' + 'murdered|exploded' + ')', item)
#         #m = re.findall(r'(' + '\\bmurder\\b' + ')', itemStr)
#         if len(m) > 0:
#             found_murder = True
#
#         m = re.findall(r'(' + '\\binjured\\b' + ')', item)
#         if len(m) > 0:
#             for j in range(i, 0, -1):
#                 victim = ne_tree[j]
#                 person = '\(PERSON\s.+\)'
#                 person = '\(FACILITY\s.+\)'
#                 entitiesperson = re.match(r'{0}'.format(person), str(victim))
#                 if entitiesperson != None:
#                     res = ''
#                     for t in victim:
#                         res += t[0] + ' '
#
#                     print(res[:-1])
#                     return res[:-1]
#
#         if found_murder and not isinstance(ne, tuple):
#             person = '\(PERSON\s.+\)'
#             facility = '\(FACILITY\s.+\)'
#
#             # person = 'PERSON'
#             # facility = 'FACILITY'
#
#             regex = '{0}|{1}'.format(person, facility)
#
#             #entitiesperson = re.match(r'{0}|{1}'.format(person, facility), str(ne))
#             entitiesperson = re.match(r'\(FACILITY\s.+\)', str(ne).replace('\n', ''))
#
#             if entitiesperson != None:
#                 res = ''
#                 for t in ne:
#                     res += t[0] + ' '
#
#                 print(res[:-1])
#                 return res[:-1]
#             #found_murder = False
#
#     return '-'
#
# def get_victim(story):
#     tokenized = nltk.word_tokenize(story)
#     tagged = nltk.pos_tag(tokenized)
#     victimsBReg = get_victims_reg(pat.victimBefore)
#     victimsAReg = get_victims_reg(pat.victimAfter)
#
#     person = '\(PERSON\s.+\)'
#     organization = '\(ORGANIZATION\s.+\)'
#
#     namedEnt = nltk.ne_chunk(tagged)
#     iob_tagged = tree2conlltags(namedEnt)
#
#     ne_tree = conlltags2tree(iob_tagged)
#
#     # for i in range(0, len(ne_tree)):
#     #     item = ne_tree[i]
#     #
#     #     if not isinstance(item, tuple):
#     #         for it in item:
#     #             bef = re.match(r'(' + victimsBReg + ')', it[0].lower())
#     #             if bef != None:
#     #                 if re.match(r'.*(' + 'been|was|have' + ').*', str(ne_tree[i - 1]).lower()) != None:
#     #                     for j in range(i - 1, 0, -1):
#     #                         nextItem = ne_tree[j]
#     #
#     #                         if not isinstance(nextItem, tuple):
#     #                             entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
#     #                             if entitiesperson != None:
#     #                                 return self.formatTuple(nextItem)
#
#     victim = find_muder_victim(ne_tree)
#
#     if victim != None and len(victim) > 2:
#         res = ''
#         for v in victim[2:]:
#             res += '{0} '.format(v[0])
#         return res[:-1]
#
#     return '-'
#     #return getEntities(ne_tree)

################################################
import re

def get_victim(ne_tree):

    for i in range(0, len(ne_tree)):
        item = str(ne_tree[i]).lower()

        m = re.findall(r'(' + '\\battack\\b|\\battempt\\b|\\bassassination\\b|\\bwounded\\b|\\bkidnapped\\b|\\bvictims\\b'
                              '|\\bmurdered\\b|\\bmurderers\\b|\\bmurder\\b|\\bmassacre\\b|\\bmassacred\\b|\\bkilled\\b|'
                              '\\bdeath\\b|\\bshot\\b|\\bwere\\b|\\bdisappearance\\b' + ')', item)

        if len(m) > 0:

            if m[0] == 'attack' or m[0] == 'attempt' or m[0] == 'victims' or m[0] == 'wounded' or m[0] == 'life' or \
                            m[0] == 'assassination' or m[0] == 'were' or m[0] == 'kidnapped' or m[0] == 'massacre' or \
                            m[0] == 'murder' or m[0] == 'death'or m[0] == 'disappearance':

                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\binclude\\|\\bon\\b|\\bagainst\\b|\\bby\\b|\\bof\\b|\\binjured\\b|\\bare\\b|\\bidentified\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0 or 'include' in item:
                            if m[0] == 'murder':
                                return findFistOrganization(aPos, ne_tree)
                            return findFistOrganization(aPos + 1, ne_tree)

            # Reverse Search
            if m[0] == 'claimed' or m[0] == 'kidnapped' or m[0] == 'shot' or m[0] == 'were':
                for aPos in range(i, i + 10):
                    if aPos < len(ne_tree):
                        m1 = re.findall(r'(' + '\\bkilled\\b|\\bresponsibility\\b|\\bby\\b|\\bwounded\\b' + ')', str(ne_tree[aPos]).lower())
                        if len(m1) > 0 or m[0] == 'kidnapped':
                            return reverseSearch(aPos - 1, ne_tree)
            if m[0] == 'murdered':
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

        m = re.findall(r'(' + 'person' + ')', victim)

        if len(m) > 0 and m[0] == 'person' and not isinstance(item, tuple):
            for t in item:
                res += t[0] + ' '
            pos += 1
        else:
            break


    res = res.strip()
    res = res.replace('Murder Of', '')
    res = res.replace('Was Shot', '')
    res.strip()
    if res.strip() != '':
        print(res.strip())
    return None if res == '' else res.strip()