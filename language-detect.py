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
parser.add_argument('-s', '--size', help='Size of sample to train against', default=4000, type=int)
parser.add_argument('-b', '--block', help='Size of block to add in each iteration', default=150, type=int)
parser.add_argument('-t', '--threads', help='Number of threads to run the training algorithm in', default=1, type=int)
parser.add_argument('-f', '--testlibrary', help='The library to test against', default='wiki-languages-train')
parser.add_argument('-c', '--testcount', help='The size of the test library', default=20000, type=int)

args = parser.parse_args()

if args.name != None:
    Loader = Corpus(features = LanguageDetectFeatures())
    start = time.time()

    libraries = args.library.split(',')
    testlibraries = args.testlibrary.split(',')

    languages = [
        'en', 'vi', 'fr', 'ceb', 'sv', 
        'es', 'de', 'ru', 'zh', 'it', 
        'pt', 'sh', 'fa', 'sr', 'nl', 
        'ar', 'ja', 'war', 'pl', 'uk', 
        'id', 'ro', 'ko', 'tr', 'ca', 
        'no', 'hu', 'fi', 'cs', 'he',
        'ms', 'hy', 'da', 'hi', 'ur',
        'eu', 'zh-min-nan', 'th', 'uz', 'bn',
        'eo', 'bg', 'kk', 'be', 'sk',
        'hr', 'el', 'lt', 'et', 'mk',
        'sl', 'bs', 'gl', 'ml', 'az',
        'ka', 'lv', 'ta', 'nn', 'min',
        'la', 'vo', 'tl', 'te', 'mg',
        'cy', 'mr', 'sq', 'new', 'ce',
        'tt', 'sco', 'tg', 'zh-yue', 'arz',
        'oc', 'azb', 'af', 'ckb'
    ]

    languages = [
        'bg', 'cs', 'da', 'de', 'el', 
        'en', 'es', 'et', 'fi', 'fr', 
        'hu', 'it', 'lt', 'lv', 'nl', 
        'pl', 'pt', 'ro', 'sk', 'sl', 
        'sv', 'no'
    ]

    languages = [
        'en', 'es', 'da', 'de', 'no',
        'it', 'pl', 'nl', 'sv', 'pt'
    ]

    tests = []
    for library in testlibraries:
        tests += Loader.get_subset(args.testcount, library, languages)

    feature_data = []
    for library in libraries:
        feature_data += Loader.get_subset(args.size * len(languages), library, languages)

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
                **result,
                'libraries': libraries,
                'tested': testlibraries,
                'classifier': f'{args.name}.pickle',
                'time': str(datetime.timedelta(seconds=end - start))
            }, jsonout, indent=4, sort_keys=True)
