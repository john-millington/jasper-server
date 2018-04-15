import json
import math
import random

from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from pprint import pprint

class Corpus:
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.stemmer = PorterStemmer()

    def get(self, size, resource):
        positives = self.sample(int(round(float(size / 2))), "positive", resource)
        negatives = self.sample(int(round(float(size / 2))), "negative", resource)

        combined = []
        combined.extend(positives)
        combined.extend(negatives)

        random.shuffle(combined)

        return combined

    def get_features(self, sentence):
        tokens = self.tokenizer.tokenize(sentence.lower())
        
        features = {}
        for token in tokens:
            stemmed = self.stemmer.stem(token)
            features[stemmed] = stemmed

        return features

    def sample(self, size, type, resource):
        info = json.load(open('./data/{}/info.json'.format(resource)))
        max_chunks = int(min(info["chunks"][type], math.ceil(float(size) / info["chunk_size"])))

        resources = []
        for x in xrange(1, max_chunks + 1):
            data = json.load(open('./data/{}/chunks/{}.chunk{}.json'.format(resource, type, x)))
            for line in data["lines"]:
                resources.append([self.get_features(line["value"]), line["sentiment"]])

        return resources[1:size]