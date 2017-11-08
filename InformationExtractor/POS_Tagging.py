import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from InformationExtractor import FileReader as fr


class POSTagger:
    def generateTags(self, filename):

        filePath = fr.getPath(filename)
        if isfile(filePath):
            tokens = nltk.word_tokenize(fr.readFile(filePath))
            tagged = nltk.pos_tag(tokens)
            namedEnt = nltk.ne_chunk(tagged, binary=False)
            # namedEnt.draw()
            print(namedEnt)
            return tagged
        return None

    def tagging(self, sentence):
        ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))

        iob_tagged = tree2conlltags(ne_tree)
        print (iob_tagged)


        ne_tree = conlltags2tree(iob_tagged)
        print (ne_tree)

    def process_content(self):

        train_text = self.getTrainData()
        sample_text = fr.readFile("DEV-MUC3-0006")

        custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

        tokenized = custom_sent_tokenizer.tokenize(sample_text)

        try:
            for i in tokenized[5:]:
                words = nltk.word_tokenize(i)
                tagged = nltk.pos_tag(words)
                namedEnt = nltk.ne_chunk(tagged)
                namedEnt.draw()

        except Exception as e:
            print(str(e))

    def getTrainData(self):

        files = [f for f in listdir(fr.FILEPATH) if isfile(join(fr.FILEPATH, f))]

        data = ""
        for file in files:
            data += fr.readFile(file)

        return data

    def processLanguage(self, contentArray):
        try:
            for item in contentArray:
                tokenized = nltk.word_tokenize(item)
                tagged = nltk.pos_tag(tokenized)
                print (tagged)

                namedEnt = nltk.ne_chunk(tagged)
                namedEnt.draw()

        except Exception as e :
            print (str(e))



def main():
    posT = POSTagger()

    file = "DEV-MUC3-0006"

    #sents = posT.readFileAsArrBySent(posT.getPath(file))
    sents2 = fr.readFileAsArr(file)
    # sents = "hello world how are you doing in this halloween sir Ray Mundo"
    #sents = "Mark and John are working at Google."


    #posT.processLanguage(sents)
    #posT.processLanguage(sents2)

    print(posT.generateTags(file))

    # posT.process_content()


if __name__ == '__main__':
    main()
