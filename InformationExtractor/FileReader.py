from os.path import isfile, join

FILEPATH = "../developset/texts/"


def readFileAsArr(filename):
    filename = getPath(filename)
    tokens = []
    with open(filename, 'r') as f:
        for line in f:
            #tokens.append(line.lower())
            tokens.append(line)
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

def getPath(filename):
    return join(FILEPATH, filename)

def readFile(filename):
    tokens = ""
    with open(filename, 'r') as f:
        for line in f:
            tokens += line
    return tokens.lower()
