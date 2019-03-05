import math

from classifiers.Classifier import Classifier
from trainers.ProbDist import ProbDist

EMOTION_CARDINALS = {
    'anger': 0,
    'fear': 0,
    'joy': 2,
    'sadness': 0,
    'love': 2,
    'surprise': 1
}

class SpecialClassifier(Classifier):
    TYPE = 'special'

    def prob_classify(self, features):
        keys = sorted(self.classifiers.keys())
        results = [1] * len(keys)

        mixed = [ 0.00001, 0.00001, 0.00001 ]
        for (key_index, layer) in enumerate(keys):
            result = self.classifiers[layer].prob_classify(features)
            layer_prob = result.prob(layer)

            results[key_index] = layer_prob

            if (layer_prob > 0.5):
                cardinal = EMOTION_CARDINALS[layer]
                if (layer_prob / 2) > mixed[cardinal]:
                    mixed[cardinal] = layer_prob / 2


        results.append(0.5)
        keys.append('neutral')

        results.append(sum(mixed))
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