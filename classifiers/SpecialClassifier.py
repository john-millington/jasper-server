import math

from classifiers.Classifier import Classifier
from trainers.ProbDist import ProbDist

class SpecialClassifier(Classifier):
    TYPE = 'special'

    # def prob_classify(self, features):
    #     keys = sorted(self.classifiers.keys())
    #     results = [1] * len(keys)

    #     mixed = 0
    #     for (key_index, layer) in enumerate(keys):
    #         result = self.classifiers[layer].prob_classify(features)
    #         results[key_index] = (result.prob(layer) * len(results))
    #         mixed += result.prob(layer)

    #     results.append(mixed)
    #     keys.append('mixed')

    #     for (index, value) in enumerate(results):
    #         results[index] = math.exp(value)
            
    #     totals = sum(results)
    #     for (index, value) in enumerate(results):
    #         results[index] = (value / totals)

    #     copied_results = results[:]
    #     max_result = max(copied_results)
    #     copied_results.remove(max_result)
        
    #     confidence = (max_result - max(copied_results))

    #     return ProbDist(dict(zip(keys, results)), confidence)