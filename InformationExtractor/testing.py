import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from InformationExtractor import IO as io
from os import listdir
from os.path import isfile, join
import re

# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")

# train_text = io.readFiles(["DEV-MUC3-0012", "DEV-MUC3-0014", "DEV-MUC3-0023", "DEV-MUC3-0025", "DEV-MUC3-0033", "DEV-MUC3-0042"])
# sample_text = io.readFile("DEV-MUC3-0006")
#
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         #for i in tokenized:
#         words = nltk.word_tokenize(sample_text)
#         tagged = nltk.pos_tag(words)
#         print (tagged)
#         namedEnt = nltk.ne_chunk(tagged)
#         namedEnt.draw()
#     except Exception as e:
#         print(str(e))
#

# process_content()

incidents = ['arson', 'attack', 'bombing', 'kidnapping', 'robbery']


def createRegex(regDict):
    res = ''
    for k, v in regDict.items():
        for item in v:
            res += '{0}|'.format(item)
    return res[:-1]


def getIncident():
    onlyfiles = [f for f in listdir(io.FILEPATH) if isfile(join(io.FILEPATH, f))]

    regex = createRegex(io.readRegex())

    print(len(onlyfiles))
    filesMatched = []
    filesNotMatched = []
    matched = False
    for file in onlyfiles:
        content = io.readFile(file).lower()

        words = nltk.word_tokenize(content)

        for word in words:
            #r = re.compile(r'\barson\b|\battack\b|\bbomb\b|\bkidnapping\b|\brobbery\b', flags=re.I | re.X)
            #m = re.match(r'(arson|attack|bomb|kidnapping|robbery|explode|taken|robbed|fire|firing|explosive|grenade)', word)
            m = re.match(r'(' + regex + ')', word)
            if m != None:
                print('{0}: {1}'.format(file, m.group(0)))  # getIncident()
                filesMatched.append(m.group(0))
                matched = True
                break
        if not matched:
            filesNotMatched.append(file)
        matched = False

    return filesMatched, filesNotMatched

ins, non = getIncident()
print(len(ins))
print(len(non))

print(non)
