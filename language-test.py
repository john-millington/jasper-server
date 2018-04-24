import pickle
import argparse

from corpus.LanguageDetectFeatures import LanguageDetectFeatures

parser = argparse.ArgumentParser()
parser.add_argument('--classifier', help='Path to the pickled classifier object')
parser.add_argument('--text', help='Text to classify')

args = parser.parse_args()
if args.classifier != None and args.text != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    text = args.text
    FeatureDetection = LanguageDetectFeatures()
    features = FeatureDetection.get(text)

    classification = classifier.classify(features)
    print(classification)

    probabilities = classifier.prob_classify(features)
    print(probabilities.dict())
    print(f"Confidence: {probabilities.confidence()}")