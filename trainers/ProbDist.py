import operator

class ProbDist:
    def __init__(self, dict, confidence):
        self.dict = dict
        self._confidence = confidence

    def confidence(self):
        return self._confidence

    def prob(self, sample):
        return self.dict.get(sample)

    def max(self):
        return max(self.dict.items(), key=operator.itemgetter(1))[0]