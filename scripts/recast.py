import pickle
import argparse

from classifiers.LanguageClassifier import LanguageClassifier
from classifiers.SentimentClassifier import SentimentClassifier
from classifiers.SpecialClassifier import SpecialClassifier

parser = argparse.ArgumentParser()
parser.add_argument('--classifier', help='Path to the pickled classifier object')
parser.add_argument('--name', help='Name of the classifier output')
parser.add_argument('--type', help='Type of classifier to create')

types = {
    'language': LanguageClassifier,
    'sentiment': SentimentClassifier,
    'special': SpecialClassifier
}

args = parser.parse_args()
if args.classifier != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    cast_to = types[args.type]
    recast = classifier.recast(cast_to)

    output = open(f'classifiers/pickled/{args.name}.pickle', 'wb')
    pickle.dump(recast, output)
    output.close()