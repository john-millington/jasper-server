import json
import math
import random

from corpus.Contractions import Contractions
from corpus.Features import Features

class Corpus:
    def __init__(self):
        self.features = Features()

    def get(self, size, resource, mutate = False):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))
        division = len(info["chunks"].keys())
        
        combined = []
        for resource_type in info["chunks"]:
            resources = self.sample(int(round(float(size / division))), resource_type, resource, mutate)
            combined.extend(resources)

        random.shuffle(combined)

        return combined

    def sample(self, size, type, resource, mutate = False):
        info = json.load(open('./corpus/data/{}/info.json'.format(resource)))
        max_chunks = int(min(info["chunks"][type], math.ceil(float(size) / info["chunk_size"])))

        resources = []
        for x in range(1, max_chunks + 1):
            data = json.load(open('./corpus/data/{}/chunks/{}.chunk{}.json'.format(resource, type, x)))
            for line in data["lines"]:
                if 'value' in line and 'classification' in line:
                    resources.append([self.features.get(line["value"]), line['classification']])

        return resources[0:size]