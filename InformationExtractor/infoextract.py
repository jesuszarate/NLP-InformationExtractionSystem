import sys
from nltk.corpus import wordnet
from pathlib import Path

FILEPATH = "devetexts/answers/texts/"


class infoExtract:
    def __init__(self, filename):
        self.tokens = self.readFile(filename)

    def readFile(self, filename):
        tokens = []
        with open(filename, 'r') as f:
            for line in f:
                tokens.extend(line.split())
        return tokens


def getFilePath(filename):
    return FILEPATH + filename


def isFile(filename):
    file = Path(getFilePath(filename))
    if file.is_file():
        return True
    return False


def main(argv):
    if len(argv) != 1:
        print('python infoextract.py <textfile>')
        print('Note: Make sure the input files are stored in the eval-program-files folder')
        sys.exit(2)

    if not (isFile(argv[0])):
        print('In argument 1 file does not exist: {0}'.format(argv[0]))
        print('Note: Make sure the input files are stored in the developset/texts/ folder')
        sys.exit(2)

    ie = infoExtract(getFilePath(argv[0]))

if __name__ == '__main__':

    syns = wordnet.synsets("playing")

    print(syns[0].name())
    print(syns[0].lemmas()[0].name())

    print(syns[0].definition())

    synonyms = []
    antonyms = []

    for syn in wordnet.synsets("good"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(synonyms)
    print(antonyms)

    main(sys.argv[1:])
