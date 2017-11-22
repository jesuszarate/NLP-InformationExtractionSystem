from pathlib import Path
from os import listdir
from os.path import isfile, join
import copy

import re

FILEPATH = "../developset/texts/"
ANSWER_FILEPATH = "../developset/answers/"
weapons = ""

ID = {'label': 'ID', 'tabs': 5}
INCIDENT = {'label': 'INCIDENT', 'tabs': 3}
WEAPON = {'label': 'WEAPON', 'tabs': 4}
PERP_INDIV = {'label': 'PERP INDIV', 'tabs': 3}
PERP_ORG = {'label': 'PERP ORG', 'tabs': 3}
TARGET = {'label': 'TARGET', 'tabs': 4}
# ELECTRIC_TOWERS = {'label': 'ELECTRIC TOWERS', 'tabs': 1}
VICTIM = {'label': 'VICTIM', 'tabs': 4}

TABS = {
    'ID': 5,
    'INCIDENT': 3,
    'WEAPON': 4,
    'PERP INDIV': 3,
    'PERP ORG': 3,
    'TARGET': 4,
    'VICTIM': 4}

FileOutputTemplate = {
    'ID': '-',
    'INCIDENT': '-',
    'WEAPON': '-',
    'PERP INDIV': '-',
    'PERP ORG': '-',
    'TARGET': '-',
    'VICTIM': '-'
}


def getTemplate():
    return copy.deepcopy(FileOutputTemplate)


def read_file_as_arr(filename):
    filename = get_path(filename)
    tokens = []
    with open(filename, 'r') as f:
        for line in f:
            # tokens.append(line.lower())
            tokens.append(line.title())
    return tokens


def read_file_as_arr_by_sent(filename):
    filename = get_path(filename)
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


def is_file(filename):
    file = Path(get_path(filename))
    if file.is_file():
        return True
    return False


def get_path(filename):
    return join(FILEPATH, filename)


def read_regex():
    categories = dict()
    with open('InformationExtractor/AttackTypes', ) as f:

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
    if path == '':
        filename = get_path(filename)
    else:
        filename = join(path, filename)

    tokens = ""
    with open(filename, 'r') as f:
        for line in f:
            tokens += line
    return tokens.title()


def read_files(filenames):
    text = ''
    for filename in filenames:
        text += readFile(filename)
    return text


def write_template(outputResults, filename):
    # filename = 'OutputFiles/{0}.templates'.format(filename)
    filename = '{0}.templates'.format(filename)
    with open(filename, 'w') as of:
        for result in outputResults:
            for key, val in result.items():
                of.write('{0}:{1}{2}\n'.format(key, '\t' * TABS[key], val))
            of.write("\n")


def read_all_files():
    files = [f for f in listdir(ANSWER_FILEPATH) if isfile(join(ANSWER_FILEPATH, f))]

    stories = []
    for file in files:
        stories.append(readFile(file, ANSWER_FILEPATH))
    return stories


def write_weapons(weapons):
    filename = 'InformationExtractor/weapons.txt'
    with open(filename, 'w') as of:
        for w in weapons:
            of.write('{0}\n'.format(w))


def get_weapons():
    weaponRegex = ''
    # with open('weapons.txt', 'r') as f:
    with open('InformationExtractor/weapons.txt', 'r') as f:
        for line in f:
            weaponRegex += '{0}|'.format(line.strip())
    return weaponRegex[:-1]