from InformationExtractor import IO as io
import nltk
import re

def createRegex(regDict):
    res = ''
    for k, v in regDict.items():
        for item in v:
            res += '(\\b{0}\\b)|'.format(item)
    return res#[:-1]

def get_incident(story):
    regexValues = io.read_regex()
    regex = createRegex(regexValues)
    print(regex)

    content = story.lower()
    words = nltk.word_tokenize(content)

    for word in words:
        m = re.match(r'(' + regex + ')', word)
        if m != None:
            val = m.group(0)
            for k, vals in regexValues.items():
                if val == 'taken':
                    return 'ATTACK'
                if val in vals:
                    return k.upper()

    return 'ATTACK'