import pickle
import time
import datetime
import argparse
import random
import json

from corpus.Corpus import Corpus
from trainers.MultilayeredRecursiveRegression import MultilayeredRecursiveRegression
from trainers.RecursiveRegressionClassifier import RecursiveRegressionClassifier

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='Name of the classifier - it will be saved to a file named the same under the trainers/trained path', required=True)
parser.add_argument('-l', '--library', help='Name of the library to train against', default='sentiment140')
parser.add_argument('-s', '--size', help='Size of sample to train against', default=10000, type=int)
parser.add_argument('-b', '--block', help='Size of block to add in each iteration', default=100, type=int)
parser.add_argument('-t', '--threads', help='Number of threads to run the training algorithm in', default=1, type=int)
parser.add_argument('-f', '--testlibrary', help='The library to test against', default='reviews,tweets')
parser.add_argument('-c', '--testcount', help='The size of the test library', default=3000, type=int)

args = parser.parse_args()

if args.name != None:
    Loader = Corpus()
    start = time.time()

    libraries = args.library.split(',')
    testlibraries = args.testlibrary.split(',')

    tests = []
    for library in testlibraries:
        tests += Loader.of_each(args.testcount, library)

    feature_data = []
    for library in libraries:
        feature_data += Loader.of_each(args.size, library)

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

        del result['classifier']
        for classification in result:
            if 'set' in result[classification]:
                result[classification]['document_count'] = len(result[classification]['set'])
                del result[classification]['set']


        with open(f'trainers/trained/{args.name}.json', 'w') as jsonout:
            json.dump({
                'libraries': libraries,
                'tested': testlibraries,
                'classifier': f'{args.name}.pickle',
                'time': str(datetime.timedelta(seconds=end - start)),
                'statistics': result
            }, jsonout, indent=4, sort_keys=True)
