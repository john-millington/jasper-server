import nltk
import pickle
import argparse
import time

from corpus.Corpus import Corpus

def test(classifier, test_set):
    start_time = time.clock()
    incorrect = 0
    outcomes = {}
    classifications = {}

    for test in test_set:
        outcome = classifier.classify(test[0])
        if test[1] not in classifications:
            classifications[test[1]] = 0

        if test[1] not in outcomes:
            outcomes[test[1]] = {}

        if outcome not in outcomes[test[1]]:
            outcomes[test[1]][outcome] = 0

        classifications[test[1]] += 1
        if (outcome != test[1]):
            outcomes[test[1]][outcome] += 1
            incorrect += 1

    accuracy = 1 - (float(incorrect) / len(test_set))
    time_taken = time.clock() - start_time
    ops_per_second = round(1 / (time_taken / len(test_set)))

    print(f"Accuracy: {accuracy * 100}%")
    print(f"Time: {time_taken}")
    print(f"Operations Run: {len(test_set)}")
    print(f"Operations/s: {ops_per_second}")
    print()
    print(outcomes)

    # for classification in classifications:
    #     cls_accuracy = 1 - (float(outcomes[classification]) / classifications[classification])
    #     print(f"{classification} accuracy: {cls_accuracy}")


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--classifier', help='Path to the pickled classifier object')
parser.add_argument('-l', '--library', help='Name of library to test against', default='reviews')
parser.add_argument('-s', '--size', help='Number of tests to run', default=3000, type=int)
parser.add_argument('-m', '--mutate', help='Mutate the sentiment based on the score attribute', default=False, type=bool)

args = parser.parse_args()
if args.classifier != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    Loader = Corpus()
    test_set = Loader.get(args.size, args.library, args.mutate)

    test(classifier, test_set)