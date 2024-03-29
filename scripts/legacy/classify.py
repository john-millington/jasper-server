import pickle
import argparse

from corpus.SentimentFeatures import SentimentFeatures

parser = argparse.ArgumentParser()
parser.add_argument('--classifier', help='Path to the pickled classifier object')
parser.add_argument('--text', help='Text to classify')

args = parser.parse_args()
if args.classifier != None and args.text != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    CorpusFeatures = SentimentFeatures()

    text = args.text
    features = CorpusFeatures.get(text)

    classification = classifier.classify(features)
    print(classification)

    probabilities = classifier.prob_classify(features)
    print(f"Positive: {probabilities.prob('positive')}")
    print(f"Negative: {probabilities.prob('negative')}")
    print(f"Neutral: {probabilities.prob('neutral')}")
    print(f"Mixed: {probabilities.prob('mixed')}")
    print(f"Confidence: {probabilities.confidence()}")