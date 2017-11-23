import nltk
import re
from InformationExtractor import Patterns as pat
from nltk.chunk import conlltags2tree, tree2conlltags

def find_muder_victim(ne_tree):
    for item in ne_tree:
        person = '\(PERSON\s.+\)'
        organization = '\(ORGANIZATION\s.+\)'
        entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
        if entitiesperson != None:
            itemStr = str(item).lower()

            m = re.findall(r'(' + 'murder' + ')', itemStr)
            #m = re.findall(r'(' + '\\bmurder\\b' + ')', itemStr)
            if len(m) > 0:
                return item
            # m = re.findall(r'(' + 'were injured' + ')', itemStr)

            # if len(m) > 0:
            #     return item

def get_victims_reg(items):
    res = ''
    for v in items:
        res += '{0}|'.format(v)
    return res[:-1]


def getEntities(ne_tree):

    found_murder = False
    #for ne in ne_tree:
    for i in range(0, len(ne_tree)):
        ne = ne_tree[i]
        item = str(ne).lower()
        m = re.findall(r'(' + 'murdered|exploded' + ')', item)
        #m = re.findall(r'(' + '\\bmurder\\b' + ')', itemStr)
        if len(m) > 0:
            found_murder = True

        m = re.findall(r'(' + '\\binjured\\b' + ')', item)
        if len(m) > 0:
            for j in range(i, 0, -1):
                victim = ne_tree[j]
                person = '\(PERSON\s.+\)'
                person = '\(FACILITY\s.+\)'
                entitiesperson = re.match(r'{0}'.format(person), str(victim))
                if entitiesperson != None:
                    res = ''
                    for t in victim:
                        res += t[0] + ' '

                    print(res[:-1])
                    return res[:-1]

        if found_murder and not isinstance(ne, tuple):
            person = '\(PERSON\s.+\)'
            facility = '\(FACILITY\s.+\)'

            # person = 'PERSON'
            # facility = 'FACILITY'

            regex = '{0}|{1}'.format(person, facility)

            #entitiesperson = re.match(r'{0}|{1}'.format(person, facility), str(ne))
            entitiesperson = re.match(r'\(FACILITY\s.+\)', str(ne).replace('\n', ''))

            if entitiesperson != None:
                res = ''
                for t in ne:
                    res += t[0] + ' '

                print(res[:-1])
                return res[:-1]
            #found_murder = False

    return '-'

def get_victim(story):
    tokenized = nltk.word_tokenize(story)
    tagged = nltk.pos_tag(tokenized)
    victimsBReg = get_victims_reg(pat.victimBefore)
    victimsAReg = get_victims_reg(pat.victimAfter)

    person = '\(PERSON\s.+\)'
    organization = '\(ORGANIZATION\s.+\)'

    namedEnt = nltk.ne_chunk(tagged)
    iob_tagged = tree2conlltags(namedEnt)

    ne_tree = conlltags2tree(iob_tagged)

    # for i in range(0, len(ne_tree)):
    #     item = ne_tree[i]
    #
    #     if not isinstance(item, tuple):
    #         for it in item:
    #             bef = re.match(r'(' + victimsBReg + ')', it[0].lower())
    #             if bef != None:
    #                 if re.match(r'.*(' + 'been|was|have' + ').*', str(ne_tree[i - 1]).lower()) != None:
    #                     for j in range(i - 1, 0, -1):
    #                         nextItem = ne_tree[j]
    #
    #                         if not isinstance(nextItem, tuple):
    #                             entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
    #                             if entitiesperson != None:
    #                                 return self.formatTuple(nextItem)

    victim = find_muder_victim(ne_tree)

    if victim != None and len(victim) > 2:
        res = ''
        for v in victim[2:]:
            res += '{0} '.format(v[0])
        return res[:-1]

    return '-'
    #return getEntities(ne_tree)