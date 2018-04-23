import math

from classifiers.Classifier import Classifier
from trainers.ProbDist import ProbDist

class LanguageClassifier(Classifier):
    def __init__(self):
        self.type = 'language'

    def prob_classify(self, features):
        keys = sorted(self.classifiers.keys())
        results = [1] * len(keys)

        for (key_index, layer) in enumerate(keys):
            result = self.classifiers[layer].prob_classify(features)
            results[key_index] = result.prob(layer)

        for (index, value) in enumerate(results):
            results[index] = math.exp(value)
            
        totals = sum(results)
        for (index, value) in enumerate(results):
            results[index] = (value / totals)

        copied_results = results[:]
        max_result = max(copied_results)
        copied_results.remove(max_result)
        
        confidence = (max_result - max(copied_results))

        return ProbDist(dict(zip(keys, results)), confidence)
