import math
from trainers.ProbDist import ProbDist

class Classifier:
  def __init__(self, classifiers): 
    self.classifiers = classifiers

  def prob_classify(self, features):
        keys = sorted(self.classifiers.keys())
        results = [1] * len(keys)

        untagged = 0
        mixed_prob = 0

        for (key_index, layer) in enumerate(keys):
            result = self.classifiers[layer].prob_classify(features)

            untagged = (untagged + result.prob('untagged_label')) / 2
            for_layer = result.prob(layer)
            if (for_layer > 0.7):
                mixed_prob = mixed_prob + (for_layer * len(results))

            polarity = for_layer - untagged

            for (result_index, value) in enumerate(results):
                if result_index == key_index:
                    # results[inner_index] = max(0.01, result.prob(layer) + polarity)
                    results[result_index] = (value + (result.prob(layer) * len(results)))
                    # results[inner_index] = result.prob(layer)
                else:
                    results[result_index] = (value + untagged)

        results.append(mixed_prob)
        keys.append('mixed')

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
