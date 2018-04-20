import json
import math
import random

from corpus.Contractions import Contractions
from corpus.SentimentFeatures import SentimentFeatures

class Corpus:
    def __init__(self, features = SentimentFeatures()):
        self.features = features

    def get(self, size, resource):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))
        division = int(round(float(size / len(info["chunks"].keys()))))

        return self.of_each(division, resource)

    def get_subset(self, size, resource, subset):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))
        division = int(round(float(size / len(subset))))

        combined = []
        for resource_type in subset:
            resources = self.sample(division, resource_type, resource)
            combined.extend(resources)

        random.shuffle(combined)

        return combined

    def of_each(self, size, resource):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))

        combined = []
        for resource_type in info['chunks']:
            resources = self.sample(size, resource_type, resource)
            combined.extend(resources)

        random.shuffle(combined)

        return combined

    def sample(self, size, type, resource):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))
        max_chunks = int(min(info["chunks"][type], math.ceil(float(size) / info["chunk_size"])))

        resources = []
        for x in range(1, max_chunks + 1):
            data = json.load(open('./corpus/data/{}/chunks/{}.chunk{}.json'.format(resource, type, x)))
            for line in data["lines"]:
                if 'value' in line and 'classification' in line:
                    resources.append([self.features.get(line["value"]), line['classification']])

        return resources[0:size]