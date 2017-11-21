from InformationExtractor import IO as io
import nltk
import re

def createRegex(regDict):
    res = ''
    for k, v in regDict.items():
        for item in v:
            res += '{0}|'.format(item)
    return res[:-1]

def get_incident(story):
    regexValues = io.read_regex()
    regex = createRegex(regexValues)

    content = story.lower()
    words = nltk.word_tokenize(content)

    for word in words:
        m = re.match(r'(' + regex + ')', word)
        if m != None:
            val = m.group(0)
            for k, vals in regexValues.items():
                if val in vals:
                    return k.upper()
            break
    return 'Attack'