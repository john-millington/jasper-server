import operator

class ProbDist:
    def __init__(self, dict):
        self.dict = dict

    def prob(self, sample):
        return self.dict.get(sample)

    def max(self):
        return max(self.dict.items(), key=operator.itemgetter(1))[0]