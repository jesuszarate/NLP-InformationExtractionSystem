from InformationExtractor import IO as io
import nltk
import re


def createRegex(regDict):
    res = ''
    for k, v in regDict.items():
        for item in v:
            res += '(\\b{0}\\b)|'.format(item)
    return res[:-1]


regexValues = io.read_regex()
regex = createRegex(regexValues)


def get_incident(story):
    content = story.lower()
    words = nltk.word_tokenize(content)

    l = {}
    res = 'ATTACK'
    for word in words:
        m = re.match(r'(' + regex + ')', word)
        if m != None:
            val = m.group(0)
            for k, vals in regexValues.items():
                if val in vals:

                    if val not in l:
                        l[k.upper()] = 0
                    l[k.upper()] += 1

    max_key = res
    if len(l) > 0:
        max_key = max(l, key=lambda k: l[k])

    if max_key != 'ATTACK':
        return max_key

    if len(l) > 1:
        del l[max_key]
        max_key = max(l, key=lambda k: l[k])

    return max_key
