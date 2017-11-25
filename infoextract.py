import sys
import re
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags

from InformationExtractor import extract_target, \
    extract_perp_org, \
    extract_perp_indiv, \
    extract_weapon, \
    extract_incident, \
    extract_victim
from InformationExtractor import IO as io

FILEPATH = "/"
ID_PATTERN = '(Dev-Muc\d+-[a-zA-Z0-9_]+)|(Tst\d+-Muc\d+-[a-zA-Z0-9_]+)'


class infoExtract:
    def __init__(self, filename):
        self.templates = []
        self.file = io.read_file_as_arr(filename)
        self.stories = self.split_stories(self.file)

        self.weapons = []



    def split_stories(self, file):
        stories = []
        current = ''
        for story in file:
            if bool(re.search(ID_PATTERN, story)) and current != '':
                stories.append(current)
                current = ''
            current += story
        stories.append(current)
        return stories

    def get_id(self, story):
        m = re.search(ID_PATTERN, story)
        return m.group(0)

    def get_victims_reg(self, items):
        res = ''
        for v in items:
            res += '{0}|'.format(v)
        return res[:-1]

    def format_tuple(self, tup):
        res = ''
        for v in tup:
            res += '{0} '.format(v[0])
        return res[:-1]

    def compute(self):

        print('computing...')
        for story in self.stories:

            tokenized = nltk.word_tokenize(story)
            tagged = nltk.pos_tag(tokenized)

            namedEnt = nltk.ne_chunk(tagged)
            iob_tagged = tree2conlltags(namedEnt)

            ne_tree = conlltags2tree(iob_tagged)

            template = io.getTemplate()
            template[io.ID['label']] = self.get_id(story).upper()
            template[io.WEAPON['label']] = extract_weapon.get_weapons(self.weapons, story).upper()
            template[io.PERP_INDIV['label']] = extract_perp_indiv.get_perp_indiv(ne_tree).upper()
            template[io.PERP_ORG['label']] = extract_perp_org.getPerpOrg().upper()
            template[io.TARGET['label']] = extract_target.getTarget(ne_tree).upper()
            template[io.INCIDENT['label']] = extract_incident.get_incident(story).upper()
            template[io.VICTIM['label']] = extract_victim.get_victim(ne_tree).upper()
            # template[io.VICTIM['label']] = extract_victim.get_victim(story).upper()
            self.templates.append(template)
        print('finished!')

    def get_results(self):
        return self.templates

    def create_regex(self, regDict):
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

    if not (io.is_file(argv[0])):
        print('In argument 1 file does not exist: {0}'.format(argv[0]))
        sys.exit(2)

    ie = infoExtract(argv[0])
    ie.compute()

    io.write_template(ie.get_results(), argv[0])


if __name__ == '__main__':
    main(sys.argv[1:])
