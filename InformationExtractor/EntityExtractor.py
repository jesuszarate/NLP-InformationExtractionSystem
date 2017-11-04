import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
from InformationExtractor import FileReader as fr

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

file = "DEV-MUC3-0006"
#contentArray = fr.readFileAsArr(file) # Uncomment this line to read the file "DEV-MUC3-0006"

##let the fun begin!##
def getGroupedEntities():
    ne_tree = None
    labeled = dict()
    try:

        for item in contentArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            # print (tagged)

            namedEnt = nltk.ne_chunk(tagged) # This creates the named entities
            # namedEnt.draw() # If you uncomment this part you'll be able to visualize it with a tree graph of the sentence

            iob_tagged = tree2conlltags(namedEnt) # Need the IOB tags in order to create the Name Entity tree
            # print (iob_tagged)

            ne_tree = conlltags2tree(iob_tagged) # This makes a Name Entity Tree
            # print(ne_tree)

            getMostCommonNE(ne_tree, labeled)

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
                curr += token
                if t + 1 > len(comTokenized):
                    curr += 'OMG '
                else:
                    curr += ' {0}'.format(comTokenized[t + 1])
                entities.append(curr)

    return entities


def main():
   grouped = getGroupedEntities()
   entities = getWordsBeforeAfterEntity(groupEntities=grouped)
   print(entities)

if __name__ == '__main__':
    main()
