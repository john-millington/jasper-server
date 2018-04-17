import math
import nltk
import os

class RegressionClassifier:
    def __init__(self, config):
        self.config = config
        self.base_data = config["base_data"]
        self.block_size = config["block_size"]
        self.feature_data = config["feature_data"]
        self.test_data = config["test_data"]

        self.score = 0
        self.iteration_score = 0

    def chunks(self):
        return [self.feature_data[i:i + self.block_size] for i in range(0, len(self.feature_data), self.block_size)]

    def test(self, classifier):
        incorrect = 0

        for test in self.test_data:
            outcome = classifier.classify(test[0])
            if (outcome != test[1]):
                incorrect += 1

        return 1 - (float(incorrect) / len(self.test_data))

    def regress(self, best_set, best_score, iteration = 0):
        classifier = None

        for i in range(0, len(best_set)):
            clone = best_set[:]
            del clone[i]

            os.system('clear')
            print("Regression Iteration: {}".format(iteration + i))
            print("Best Score: {}".format(best_score))

            classifier = nltk.NaiveBayesClassifier.train(clone)
            score = self.test(classifier)
            if (score > best_score):
                best_score = score
                best_set = clone

                return self.regress(best_set, best_score, iteration + i)

        return {
            "classifier": classifier,
            "set": best_set,
            "score": best_score
        }

    def train(self):
        best_score = 0
        best_set = []
        chunks = self.chunks()

        for i in range(0, len(chunks)):
            base_clone = self.base_data[:] + chunks[i]
            classifier = nltk.NaiveBayesClassifier.train(base_clone)

            score = self.test(classifier)
            if (score > best_score):
                best_score = score
                best_set = base_clone

            os.system('clear')
            print("Iteration: {}".format(i))
            print("Best Score: {}".format(best_score))

        return self.regress(best_set, best_score)

        