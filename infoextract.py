import sys
import nltk
import re
from nltk.chunk import conlltags2tree, tree2conlltags
from InformationExtractor import extract_target, extract_perp_org, extract_perp_indiv, extract_weapon
from InformationExtractor import IO as io
from InformationExtractor import Patterns as pat

# FILEPATH = "devetexts/answers/texts/"
FILEPATH = "/"

ID_PATTERN = '(Dev-Muc\d+-[a-zA-Z0-9_]+)|(Tst\d+-Muc\d+-[a-zA-Z0-9_]+)'


class infoExtract:
    def __init__(self, filename):
        self.templates = []
        self.file = io.readFileAsArr(filename)
        self.stories = self.splitStories(self.file)

        self.weapons = []

    def splitStories(self, file):
        stories = []
        current = ''
        for story in file:
            if bool(re.search(ID_PATTERN, story)) and current != '':
                stories.append(current)
                current = ''
            current += story
        stories.append(current)
        return stories

    def getID(self, story):
        m = re.search(ID_PATTERN, story)
        return m.group(0)

    def getVictimsReg(self, items):
        res = ''
        for v in items:
            res += '{0}|'.format(v)
        return res[:-1]

    def findMuderVictim(self, ne_tree):

        for item in ne_tree:
            person = '\(PERSON\s.+\)'
            organization = '\(ORGANIZATION\s.+\)'
            entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
            if entitiesperson != None:
                itemStr = str(item).lower()

                m = re.findall(r'(' + '.*murder/.*' + ')', itemStr)
                if len(m) > 0:
                    return item

    def formatTuple(self, tup):
        res = ''
        for v in tup:
            res += '{0} '.format(v[0])
        return res[:-1]


    def getVictim(self, story):
        tokenized = nltk.word_tokenize(story)
        tagged = nltk.pos_tag(tokenized)
        victimsBReg = self.getVictimsReg(pat.victimBefore)
        victimsAReg = self.getVictimsReg(pat.victimAfter)

        person = '\(PERSON\s.+\)'
        organization = '\(ORGANIZATION\s.+\)'

        namedEnt = nltk.ne_chunk(tagged)
        iob_tagged = tree2conlltags(namedEnt)

        ne_tree = conlltags2tree(iob_tagged)

        # for i in range(0, len(ne_tree)):
        #     item = ne_tree[i]
        #
        #     if not isinstance(item, tuple):
        #         for it in item:
        #             bef = re.match(r'(' + victimsBReg + ')', it[0].lower())
        #             if bef != None:
        #                 if re.match(r'.*(' + 'been|was|have' + ').*', str(ne_tree[i - 1]).lower()) != None:
        #                     for j in range(i - 1, 0, -1):
        #                         nextItem = ne_tree[j]
        #
        #                         if not isinstance(nextItem, tuple):
        #                             entitiesperson = re.match(r'{0}|{1}'.format(person, organization), str(item))
        #                             if entitiesperson != None:
        #                                 return self.formatTuple(nextItem)

        victim = self.findMuderVictim(ne_tree)

        if victim != None and len(victim) > 2:
            res = ''
            for v in victim[2:]:
                res += '{0} '.format(v[0])
            return res[:-1]
        return '-'

    def getIncident(self, story):
        regexValues = io.readRegex()
        regex = self.createRegex(regexValues)

        content = story.lower()
        words = nltk.word_tokenize(content)

        for word in words:
            m = re.match(r'(' + regex + ')', word)
            if m != None:
                val = m.group(0)
                #filesMatched.append(m.group(0))
                for k, vals in regexValues.items():
                    if val in vals:
                        return k
                break
        return 'Attack'

    def compute(self):

        for story in self.stories:
            template = io.getTemplate()
            template[io.ID['label']] = self.getID(story).upper()
            template[io.WEAPON['label']] = extract_weapon.get_weapons(self.weapons, story)
            template[io.PERP_INDIV['label']] = extract_perp_indiv.get_perp_indiv()
            template[io.PERP_ORG['label']] = extract_perp_org.getPerpOrg()
            template[io.TARGET['label']] = extract_target.getTarget()
            template[io.INCIDENT['label']] = self.getIncident(story).upper()
            template[io.VICTIM['label']] = self.getVictim(story)
            self.templates.append(template)

    def getResults(self):
        return self.templates

    def createRegex(self, regDict):
        res = ''
        for k, v in regDict.items():
            for item in v:
                res += '{0}|'.format(item)
        return res[:-1]


def main(argv):
    io.FILEPATH = ''
    if len(argv) != 1:
        print('python infoextract.py <textfile>')
        sys.exit(2)

    if not (io.isFile(argv[0])):
        print('In argument 1 file does not exist: {0}'.format(argv[0]))
        print('Note: Makesure the input file is inside of the InformationExtractor directory')
        sys.exit(2)

    ie = infoExtract(argv[0])
    ie.compute()

    io.writeTemplate(ie.getResults(), argv[0])


if __name__ == '__main__':
    main(sys.argv[1:])
