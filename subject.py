import argparse

from nltk.tree import Tree
from pycorenlp import StanfordCoreNLP

parser = argparse.ArgumentParser()
parser.add_argument('--text', help='Text to classify')
args = parser.parse_args()

nlp = StanfordCoreNLP('http://localhost:9000')
output = nlp.annotate(args.text, properties={
    'annotators': 'parse',
    'outputFormat': 'json'
})

parsed = Tree.fromstring(output['sentences'][0]['parse'])
sentence = parsed[0]
nounphrase = None
verbphrase = None

for subtree in sentence:
    if subtree.label() == 'NP':
        nounphrase = subtree.leaves()

    if (subtree.label() == 'VP'):
        verbphrase = subtree.leaves()

if (nounphrase != None and verbphrase != None):
    print(nounphrase)
    print(verbphrase)