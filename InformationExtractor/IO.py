from os.path import isfile, join
from pathlib import Path

import copy

FILEPATH = "../developset/texts/"

ID = {'label': 'ID', 'tabs': 5}
INCIDENT = {'label': 'INCIDENT', 'tabs': 3}
WEAPON = {'label': 'WEAPON', 'tabs': 4}
PERP_INDIV = {'label': 'PERP INDIV', 'tabs': 3}
PERP_ORG = {'label': 'PERP ORG', 'tabs': 3}
TARGET = {'label': 'TARGET', 'tabs': 4}
ELECTRIC_TOWERS = {'label': 'ELECTRIC TOWERS', 'tabs': 1}
VICTIM = {'label': 'VICTIM', 'tabs': 4}

TABS = {
'ID' : 5,
'INCIDENT' : 3,
'WEAPON' : 4,
'PERP_INDIV' : 3,
'PERP_ORG' : 3,
'TARGET' : 4,
'ELECTRIC_TOWERS' : 1,
'VICTIM' : 4}


FileOutputTemplate = {
    'ID': '-',
    'INCIDENT': '-',
    'WEAPON': '-',
    'PERP_INDIV': '-',
    'PERP_ORG': '-',
    'TARGET': '-',
    'ELECTRIC_TOWERS': '-',
    'VICTIM': '-'
}

def getTemplate():
    return copy.deepcopy(FileOutputTemplate)

def readFileAsArr(filename):
    filename = getPath(filename)
    tokens = []
    with open(filename, 'r') as f:
        for line in f:
            # tokens.append(line.lower())
            tokens.append(line.title())
    return tokens


def readFileAsArrBySent(filename):
    filename = getPath(filename)
    tokens = []
    prev = ""
    with open(filename, 'r') as f:
        currLine = ''
        for line in f:
            if prev != '\n':
                currLine += line
            else:
                tokens.append(currLine)
                currLine = ''
            prev = line
    return tokens


def isFile(filename):
    file = Path(getPath(filename))
    if file.is_file():
        return True
    return False


def getPath(filename):
    return join(FILEPATH, filename)

def readRegex():
    categories = dict()
    with open('AttackTypes', ) as f:

        prev = '\n'
        for line in f:
            if line == '\n':
                prev = line
                continue
            line = line.strip()
            if prev == '\n' and line not in categories:
                prev = line
                categories[prev] = set()

            categories[prev].add(line)
    return categories

def readFile(filename, path=''):
    # if path == '':
    #     filename = getPath(filename)
    # else:
    #     filename
    filename = getPath(filename)
    tokens = ""
    with open(filename, 'r') as f:
        for line in f:
            tokens += line
    # return tokens.lower()
    #print(tokens.title())

    # tokens = '. '.join(i.capitalize() for i in tokens.split('.\\s*'))
    return tokens.title()
    # return tokens.capitalize()


def readFiles(filenames):
    text = ''
    for filename in filenames:
        text += readFile(filename)
    return text


def writeTemplate(outputResults, filename):
    filename = '../OutputFiles/{0}.templates'.format(filename)
    with open(filename, 'w') as of:
        for result in outputResults:
            for key, val in result.items():
                of.write('{0}:{1}{2}\n'.format(key, '\t'*TABS[key], val))
            of.write("\n")
