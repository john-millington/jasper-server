import pickle
import argparse
import json

from corpus.Corpus import Corpus
from corpus.LanguageDetectFeatures import LanguageDetectFeatures

parser = argparse.ArgumentParser()
parser.add_argument('--classifier', help='Path to the pickled classifier object')
parser.add_argument('--library', help='Text to classify')

args = parser.parse_args()
if args.classifier != None and args.library != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    loader = Corpus(LanguageDetectFeatures())
    testset = loader.get_subset(17000, args.library, ['da', 'de', 'el', 'en', 'es', 'et', 'fi', 'fr', 'hu', 'it', 'nl', 'pl', 'pt', 'ro', 'sk', 'sl', 'sv'])

    results = {}
    for line in testset:
        classification = classifier.prob_classify(line[0])
        original = line[1]
        highest = classification.max()

        if original not in results:
            results[original] = {
                'count': 0,
                'correct': 0,
                'highest': classification.confidence(),
                'confidence': classification.confidence(),
                'lowest': classification.confidence(),
            }

        if highest not in results[original]:
            results[original][highest] = 0

        results[original][highest] += 1
        results[original]['confidence'] = (results[original]['confidence'] + classification.confidence()) / 2
        if (classification.confidence() < results[original]['lowest']):
            results[original]['lowest'] = classification.confidence()
            # results[original]['lowest_text'] = line[0]
            results[original]['lowest_classification'] = highest

        if (classification.confidence() > results[original]['highest']):
            results[original]['highest'] = classification.confidence()
            # results[original]['highest_text'] = line[0]
            results[original]['highest_classfication'] = highest

        results[original]['count'] += 1
        if original == highest:
            results[original]['correct'] += 1

    for lang in results:
        results[lang]['percentage'] = (results[lang]['correct'] / results[lang]['count']) * 100

    overall = 0
    for lang in results:
        overall += results[lang]['percentage']

    results['overall'] = overall / 17

    print(json.dumps(results, indent=4, sort_keys=True))