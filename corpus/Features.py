import json

from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

from corpus.Contractions import Contractions

cFeatures = json.load(open('./corpus/data/features.json'))

class Features:
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.stemmer = PorterStemmer()

    def get(self, sentence):
        expanded = Contractions.expand(sentence.lower())
        tokens = self.tokenizer.tokenize(expanded)
        
        features = {}
        for token in tokens:
            stemmed = self.stemmer.stem(token)
            features[f"w_{stemmed}"] = stemmed

        # for feature in cFeatures:
        #     if feature in expanded:
        #         features[cFeatures[feature]] = True

        return features