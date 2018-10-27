import math
import nltk
import os

from trainers.RegressionType import RegressionType

class RegressionClassifier:
    def __init__(self, config):
        self.config = config
        self.base_data = config["base_data"]
        self.block_size = config["block_size"]
        self.feature_data = config["feature_data"]
        self.test_data = config["test_data"]
        
        self.name = 'Untitled'
        if 'name' in config:
            self.name = config['name']
        
        self.regression_type = RegressionType.SCORE
        if 'regression_type' in config:
            self.regression_type = config['regression_type']
        
        self.iteration_score = 0

    def condition(self, previous_score, new_score):
        if self.regression_type is RegressionType.SCORE:
            return previous_score['score'] < new_score['score']
        elif self.regression_type is RegressionType.DELTA:
            return previous_score['delta'] > new_score['delta']
        elif self.regression_type is RegressionType.ABSOLUTE:
            return previous_score['score'] < new_score['score'] and previous_score['delta'] >= new_score['delta']
        elif self.regression_type is RegressionType.EQUIVALENT:
            return previous_score['score'] + previous_score['delta'] > new_score['score'] + new_score['delta']
        elif self.regression_type is RegressionType.DELTA_RANGE:
            return previous_score['score'] < new_score['score'] and (new_score['delta'] - previous_score['delta'] < 0.03)
        else:
            return previous_score['score'] < new_score['score'] or previous_score['delta'] > new_score['delta']
        

    def chunks(self):
        return [self.feature_data[i:i + self.block_size] for i in range(0, len(self.feature_data), self.block_size)]

    def test(self, classifier):
        incorrect = 0
        
        runs = {}
        deltas = {}

        for test in self.test_data:
            outcome = classifier.classify(test[0])
            expected = test[1]

            if expected not in runs:
                runs[expected] = 0

            if expected not in deltas:
                deltas[expected] = 0

            runs[expected] += 1
            if (outcome != test[1]):
                deltas[expected] += 1
                incorrect += 1

        corrections = []
        for delta in deltas:
            accuracy = 1 - (float(deltas[delta]) / runs[delta])
            corrections.append(accuracy)

        delta_calc = max(corrections) - min(corrections)
        return {
            'score': 1 - (float(incorrect) / len(self.test_data)),
            'delta': delta_calc
        } 

    def regress(self, best_set, best_score, iteration = 0):
        classifier = None
        best_set.sort(key=lambda entry:entry[1])

        for i in range(0, int(len(best_set) / 2)):
            clone = best_set[:]
            
            del clone[i]
            del clone[len(clone) - (i + 1)]

            os.system('clear')
            print('Title: {}'.format(self.name))
            print("Regression Iteration: {}".format(iteration + i))
            print("Best Score: {}".format(best_score))

            classifier = nltk.NaiveBayesClassifier.train(clone)
            score = self.test(classifier)
            if self.condition(best_score, score):
                best_score = score
                best_set = clone

                return self.regress(best_set, best_score, iteration + i)

        return {
            "classifier": classifier,
            "set": best_set,
            "score": best_score['score'],
            "delta": best_score['delta']
        }

    def train(self):
        best_score = {
            'score': 0,
            'delta': 1
        }

        best_set = []
        chunks = self.chunks()

        for i in range(0, len(chunks)):
            base_clone = self.base_data[:] + chunks[i]
            classifier = nltk.NaiveBayesClassifier.train(base_clone)

            score = self.test(classifier)
            if self.condition(best_score, score):
                best_score = score
                best_set = base_clone

            os.system('clear')
            print('Title: {}'.format(self.name))
            print("Iteration: {}".format(i))
            print("Best Score: {}".format(best_score))

        return self.regress(best_set, best_score)

        