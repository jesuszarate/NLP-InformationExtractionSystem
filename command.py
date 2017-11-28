import os


def computeTrueCase(filename):
    filename = '../{0}'.format(filename)
    olddir = os.getcwd()
    os.chdir('stanford-corenlp-full-2017-06-09')

    command = 'java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -outputFormat conll ' \
              '-annotators tokenize,ssplit,truecase,pos,lemma,ner -file {0} -truecase.overwriteText'.format(filename)

    print(os.popen(command).read())

    basename = '{0}.conll'.format(os.path.basename(filename))
    dirname = os.path.dirname(filename)
    process = os.popen('mv {0} {1}'.format(basename, dirname)).read()

    os.chdir(olddir)
