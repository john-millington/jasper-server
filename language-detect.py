import pickle
import time
import datetime
import argparse
import random
import json

from corpus.Corpus import Corpus
from corpus.LanguageDetectFeatures import LanguageDetectFeatures
from trainers.MultilayeredRecursiveRegression import MultilayeredRecursiveRegression
from trainers.RecursiveRegressionClassifier import RecursiveRegressionClassifier

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='Name of the classifier - it will be saved to a file named the same under the trainers/trained path', required=True)
parser.add_argument('-l', '--library', help='Name of the library to train against', default='wiki-languages-train')
parser.add_argument('-s', '--size', help='Size of sample to train against', default=2000, type=int)
parser.add_argument('-b', '--block', help='Size of block to add in each iteration', default=100, type=int)
parser.add_argument('-t', '--threads', help='Number of threads to run the training algorithm in', default=1, type=int)
parser.add_argument('-f', '--testlibrary', help='The library to test against', default='wiki-languages-train')
parser.add_argument('-c', '--testcount', help='The size of the test library', default=3000, type=int)

args = parser.parse_args()

if args.name != None:
    Loader = Corpus(features = LanguageDetectFeatures())
    start = time.time()

    libraries = args.library.split(',')
    testlibraries = args.testlibrary.split(',')

    tests = []
    for library in testlibraries:
        tests += Loader.get_subset(args.testcount, library, ['en', 'de', 'fr', 'es', 'it'])

    feature_data = []
    for library in libraries:
        feature_data += Loader.get_subset(args.size * 5, library, ['en', 'de', 'fr', 'es', 'it'])

    random.shuffle(feature_data)

    Classifier = MultilayeredRecursiveRegression({
        "base_data": [],
        "block_size": args.block,
        "feature_data": feature_data,
        "test_data": tests,
        "thread_count": args.threads
    })

    result = Classifier.train()
    end = time.time()

    if (result["classifier"] != None):
        output = open(f'trainers/trained/{args.name}.pickle', 'wb')
        pickle.dump(result["classifier"], output)
        output.close()

        # outcomes = {}
        # for item in result['set']:
        #     if item[1] not in outcomes:
        #         outcomes[item[1]] = 0

        #     outcomes[item[1]] += 1

        with open(f'trainers/trained/{args.name}.json', 'w') as jsonout:
            json.dump({
                'libraries': libraries,
                'tested': testlibraries,
                'en': result['en'],
                'de': result['de'],
                'fr': result['fr'],
                'it': result['it'],
                'es': result['es'],
                'classifier': f'{args.name}.pickle',
                'time': str(datetime.timedelta(seconds=end - start))
            }, jsonout, indent=4, sort_keys=True)
