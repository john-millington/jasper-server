import operator

class ProbDist:
    def __init__(self, dict, confidence):
        self._dict = dict
        self._confidence = confidence

    def confidence(self):
        return self._confidence

    def dict(self):
        return self._dict

    def prob(self, sample):
        return self._dict.get(sample)

    def max(self):
        return max(self._dict.items(), key=operator.itemgetter(1))[0]