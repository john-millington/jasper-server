import nltk
import pickle

from Corpus import Corpus
from pprint import pprint

Body = Corpus()

def test(classifier, test_set):
    incorrect = 0

    for test in test_set:
        outcome = classifier.classify(test[0])
        if (outcome != test[1]):
            incorrect += 1

    accuracy = 1 - (float(incorrect) / len(test_set))
    print(accuracy * 100)


train_set = Body.get(1600000, "sentiment140")
test_set1 = Body.get(3000, "reviews")
# test_set2 = [train_set[500:], train_set[:500]]

classifier = nltk.NaiveBayesClassifier.train(train_set)

dump = open('sentiment.pickle', 'wb')
pickle.dump(classifier, dump)
dump.close()

test(classifier, test_set1)
# test(classifier, test_set2)

# features = Body.get_features("it was a really good film")
# dists = classifier.prob_classify(features)

# print(dists.prob("positive"))
# print(dists.prob('negative'))
