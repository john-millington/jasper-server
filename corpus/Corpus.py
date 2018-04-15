import json
import math
import random

from pprint import pprint

from corpus.Contractions import Contractions
from corpus.Features import Features

class Corpus:
    def __init__(self):
        self.features = Features()

    def get(self, size, resource):
        positives = self.sample(int(round(float(size / 2))), "positive", resource)
        negatives = self.sample(int(round(float(size / 2))), "negative", resource)

        combined = []
        combined.extend(positives)
        combined.extend(negatives)

        random.shuffle(combined)

        return combined

    def sample(self, size, type, resource):
        info = json.load(open('./Corpus/data/{}/info.json'.format(resource)))
        max_chunks = int(min(info["chunks"][type], math.ceil(float(size) / info["chunk_size"])))

        resources = []
        for x in range(1, max_chunks + 1):
            data = json.load(open('./Corpus/data/{}/chunks/{}.chunk{}.json'.format(resource, type, x)))
            for line in data["lines"]:
                if 'value' in line and 'sentiment' in line:
                    resources.append([self.features.get(line["value"]), line["sentiment"]])

        return resources[1:size]