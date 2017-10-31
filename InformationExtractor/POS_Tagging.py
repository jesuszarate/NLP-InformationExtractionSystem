import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize, word_tokenize

FILEPATH = "../developset/texts/"

class POSTagger:

    def generateTags(self, filename):

        filePath = self.getPath(filename)
        if isfile(filePath):
            tokens = nltk.word_tokenize(self.readFile(filePath))
            tagged = nltk.pos_tag(tokens)
            return tagged
        return None

    def getPath(self, filename):
        return join(FILEPATH, filename)

    def readFile(self, filename):
        tokens = ""
        with open(filename, 'r') as f:
            for line in f:
                tokens += line
        return tokens.lower()

def main():
    posT = POSTagger()

    file = "DEV-MUC3-0012"
    print(posT.generateTags(file))

if __name__ == '__main__':

    main()