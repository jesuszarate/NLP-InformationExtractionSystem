import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
from InformationExtractor import IO as io
from InformationExtractor import Patterns as pat
import re

# '<subj> passive-verb'
# '<subj> active-verb'
# '<subj> verb infin.'
# '<subj> aux noun'
#
# 'passive-verb <dobj>'
# 'active-verb <dobj>'
# 'infin <dobj>'
# 'verb infin. <dobj>'
# 'gerund <dobj>'
# 'non aux <dobj>'
#
# 'noun prep <np>'
# 'active-verb prep <np>'
# 'passive-verb prep <np>'

# '<victim> was murdered'
# '<perp> bombed'
# '<perp> attempted to kill'
# '<victim> was victim'
#
# 'killed <victim>'
# 'bombed <target>'
# 'to kill <victim>'
# 'tried to attack <target>'
# 'killing <victim>'
# 'fatality was <victim>'
#
# 'bomb against <target>'
# 'killed with <instrument>'
# 'was aimed at <target>'

exampleArray = ['The incredibly intimidating NLP scares people away who are sissies.']

contentArray = ['SAN SALVADOR, 9 JAN 90 (DPA) -- [TEXT] THE SALVADORAN ARMY TODAY\
                PREVENTED THE OCCUPATION OF CITIES IN THE EASTERN PART OF EL SALVADOR\
                WAGING STRONG CLASHES BETWEEN MIDNIGHT AND DAWN, ACCORDING TO REPORTS BY\
                MILITARY SOURCES.']

contentArray = ['THE 1ST INFANTRY BRIGADE IS CARRYING OUT OPERATIONS IN NORTHERN SAN\n',
                'SALVADOR.  AND ON THE OUTSKIRTS OF THE CAPITAL THIS MORNING POWERFUL\n',
                'EXPLOSIONS, CHARACTERIZED AS MILITARY ACTIONS TO PREVENT REBELS FROM\n',
                'GATHERING, COULD BE HEARD.  THE NIGHT BEFORE LAST, THERE WERE ATTEMPTS TO\n',
                'ENTER THE CAPITAL FROM THAT DIRECTION.\n']

file = "testset1-input.txt.conll"
# contentArray = io.readFileAsArr(file) # Uncomment this line to read the file "DEV-MUC3-0006"
contentArray = [io.readFile(file)]  # Uncomment this line to read the file "DEV-MUC3-0006"


def createRegex(regDict):
    res = ''
    for k, v in regDict.items():
        res += '{0}|'.format(k)
    return res[:-1]


def createSecRegex(regDict):
    res = ''
    for k, v in regDict.items():
        res += '{0}|'.format(v)
    return res[:-1]


def getVictimsReg(items):
    res = ''
    for v in items:
        res += '{0}|'.format(v)
    return res[:-1]


##let the fun begin!##
# def look(ne_tree):
#     keyword = createRegex(pat.Location)
#
#
#     foundKey = False
#     for item in ne_tree:
#
#         if foundKey and not isinstance(item, tuple):
#             return item
#
#         if not isinstance(item, tuple):
#             for i in item:
#                 m = re.match(r'(' + keyword + ')', i[0].lower())
#                 #if keyword == i[0].lower():
#                 if m != None:
#                     val = m.group(0)
#                     foundKey = True
#                     break
#         else:
#             what = item[0]
#
#             m = re.match(r'(' + keyword + ')', what.lower())
#
#             if m != None:
#             #if keyword == what.lower():
#                 foundKey = True


# def look(ne_tree):
#     keyword = createRegex(pat.Location)
#     secRegex = createSecRegex(pat.Location)
#
#
#     foundKey = False
#     foundMatch = False
#     #for item in ne_tree:
#     for i in range(0, len(ne_tree)):
#         item = ne_tree[i]
#
#
#         if foundMatch and not isinstance(item, tuple):
#
#             entitiesperson = re.match(r'\(PERSON\s.+\)', str(item))
#             if entitiesperson != None:
#                 return item
#
#         if not isinstance(item, tuple):
#             for i in item:
#                 m = re.match(r'(' + keyword + ')', i[0].lower())
#                 if m != None:
#                     val = m.group(0)
#                     foundKey = True
#                     break
#         elif foundKey:
#             what = item[0]
#             m = re.match(r'(' + secRegex + ')', what.lower())
#             if m != None:
#                 foundMatch = True
#             foundKey = False
#         else:
#             what = item[0]
#
#             m = re.match(r'(' + keyword + ')', what.lower())
#
#             if m != None:
#                 foundKey = True

def look1(ne_tree):
    keyword = createRegex(pat.Location)
    secRegex = createSecRegex(pat.Location)
    victimsBReg = getVictimsReg(pat.victimBefore)
    victimsAReg = getVictimsReg(pat.victimAfter)

    person = '\(PERSON\s.+\)'
    organization = '\(ORGANIZATION\s.+\)'
    foundKey = False
    foundMatch = False
    # for item in ne_tree:
    for i in range(0, len(ne_tree)):
        item = ne_tree[i]

        # if foundMatch and not isinstance(item, tuple):
        #
        #     entitiesperson = re.match(r'\(PERSON\s.+\)', str(item))
        #     if entitiesperson != None:
        #         return item

        if not isinstance(item, tuple):
            for it in item:
                bef = re.match(r'(' + victimsBReg + ')', it[0].lower())
                aft = re.match(r'(' + victimsAReg + ')', it[0].lower())
                if bef != None:
                    if re.match(r'.*(' + 'been|was|have' + ').*', str(ne_tree[i - 1]).lower()) != None:

                        for j in range(i - 1, 0, -1):
                            nextItem = ne_tree[j]

                            if not isinstance(nextItem, tuple):
                                entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
                                if entitiesperson != None:
                                    return nextItem

                if aft != None:

                    if re.match(r'.*(' + 'of' + ').*', str(ne_tree[i - 1]).lower()) != None:

                        for j in range(i + 1, len(ne_tree)):
                                nextItem = ne_tree[j]
                                if not isinstance(nextItem, tuple):
                                    entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
                                    if entitiesperson != None:
                                        return nextItem


        elif foundKey:
            what = item[0]
            m = re.match(r'(' + secRegex + ')', what.lower())
            if m != None:
                foundMatch = True
            foundKey = False
        else:
            what = item[0]

            m = re.match(r'(' + victimsAReg + ')', what.lower())

            if m != None:
                for j in range(i + 1, len(ne_tree)):
                    nextItem = ne_tree[j]
                    if foundMatch and not isinstance(nextItem, tuple):

                        entitiesperson = re.match(r'\(PERSON\s.+\)', str(nextItem))
                        if entitiesperson != None:
                            return nextItem

            m = re.match(r'(' + victimsBReg + ')', what.lower())

            if m != None:
                foundKey = True


def findMuderVictim(ne_tree):
    for item in ne_tree:
        person = '\(PERSON\s.+\)'
        organization = '\(ORGANIZATION\s.+\)'
        entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
        if entitiesperson != None:
            print(item)
            itemStr = str(item).lower()
            m = re.match(r'(' + '.*murder/.*' + ')', itemStr)
            if m != None:
                print(item)


def getGroupedEntities():
    ne_tree = None
    labeled = dict()
    try:

        for item in contentArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            # print (tagged)

            namedEnt = nltk.ne_chunk(tagged)  # This creates the named entities
            # namedEnt.draw() # If you uncomment this part you'll be able to visualize it with a tree graph of the sentence

            iob_tagged = tree2conlltags(namedEnt)  # Need the IOB tags in order to create the Name Entity tree
            # print (iob_tagged)

            ne_tree = conlltags2tree(iob_tagged)  # This makes a Name Entity Tree
            print(ne_tree)

            print(look1(ne_tree))
            # findMuderVictim(ne_tree)

            # getMostCommonNE(ne_tree, labeled)

        return labeled
    except Exception as e:
        print('freaking error!')
        print(str(e))


def getMostCommonNE(ne_tree, labeled):
    for t in ne_tree:
        if not isinstance(t, tuple):
            value = t[0][0]  # + ' ' + t[0][1]
            if t.label() not in labeled:
                labeled[t.label()] = {value: 0}

            if value not in labeled[t.label()]:
                labeled[t.label()][value] = 0

            labeled[t.label()][value] += 1


def getWordsBeforeAfterEntity(groupEntities):
    # Combine into one string
    combined = ''
    for line in contentArray:
        combined += line

    comTokenized = nltk.word_tokenize(combined)

    popularBefore = dict()
    popularAfter = dict()
    entities = []
    for t in range(0, len(comTokenized)):  # token in comTokenized:
        token = comTokenized[t]
        for label in groupEntities.values():
            curr = ''
            if token in label:
                if t - 1 < 0:
                    curr += 'PHI '
                else:
                    curr += '{0} '.format(comTokenized[t - 1])
                    before = '{0} {1}'.format(comTokenized[t - 1], token)
                    if comTokenized[t - 1] not in popularBefore:
                        # popularBefore[comTokenized[t - 1]] = 0
                        popularBefore[before] = 0
                    # popularBefore[comTokenized[t - 1]] += 1
                    popularBefore[before] += 1
                curr += token
                if t + 3 > len(comTokenized):
                    curr += 'OMG '
                else:
                    curr += ' {0}'.format(comTokenized[t + 1])
                    after = '{0} {1} {2}'.format(token, comTokenized[t + 1], comTokenized[t + 2])
                    if comTokenized[t + 1] not in popularAfter:
                        # popularAfter[comTokenized[t+1]] = 0
                        popularAfter[after] = 0
                    popularAfter[after] += 1
                entities.append(curr)

    printPopular(popularBefore, 'popularBefore')
    printPopular(popularAfter, 'popularAfter')

    with open('both', 'w') as of:
        for e in entities:
            of.write(e + '\n')
    return entities


def printPopular(popular, filename):
    with open(filename, 'w') as of:
        for p, val in popular.items():
            of.write('{0} : {1}'.format(p, val))
            of.write('\n')


def main():
    grouped = getGroupedEntities()
    # entities = getWordsBeforeAfterEntity(groupEntities=grouped)
    # print(entities)


if __name__ == '__main__':
    main()
