from nltk.corpus import wordnet
from pathlib import Path
syns = wordnet.synsets("arson")

print(syns[0].name())
print(syns[0].lemmas()[0].name())

print(syns[0].definition())

synonyms = []
antonyms = []

for syn in wordnet.synsets("bomb"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(synonyms)
print(antonyms)