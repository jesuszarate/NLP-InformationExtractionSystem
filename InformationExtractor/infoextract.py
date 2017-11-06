import sys
from nltk.corpus import wordnet
from pathlib import Path
import re
from InformationExtractor import IO as io

FILEPATH = "devetexts/answers/texts/"


class infoExtract:
    def __init__(self, filename):
        # self.tokens = self.readFile(filename)
        self.template = io.FileOutputTemplate
        self.file = io.readFile(filename)

    def getID(self):
        m = re.search('[a-zA-Z0-9_]+-[a-zA-Z0-9_]+-[a-zA-Z0-9_]+', self.file)
        return m.group(0)

    def compute(self):
        self.template[io.ID['label']] = self.getID()

    def getResults(self):
        return self.template



def main(argv):
    if len(argv) != 1:
        print('python infoextract.py <textfile>')
        print('Note: Make sure the input files are stored in the eval-program-files folder')
        sys.exit(2)

    if not (io.isFile(argv[0])):
        print('In argument 1 file does not exist: {0}'.format(argv[0]))
        print('Note: Make sure the input files are stored in the developset/texts/ folder')
        sys.exit(2)

    ie = infoExtract(argv[0])
    ie.compute()

    io.writeTemplate(ie.getResults(), argv[0])

if __name__ == '__main__':

    # syns = wordnet.synsets("playing")
    #
    # print(syns[0].name())
    # print(syns[0].lemmas()[0].name())
    #
    # print(syns[0].definition())
    #
    # synonyms = []
    # antonyms = []
    #
    # for syn in wordnet.synsets("good"):
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    #         if l.antonyms():
    #             antonyms.append(l.antonyms()[0].name())
    #
    # print(synonyms)
    # print(antonyms)

    main(sys.argv[1:])
