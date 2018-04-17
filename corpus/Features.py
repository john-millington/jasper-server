import json
import re

from nltk.corpus import stopwords as StopWords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer

from corpus.Contractions import Contractions

cFeatures = json.load(open('./corpus/data/features.json'))

class Features:
    # Removes twitter mentions and the preceeding hash from hash tags
    TWITTER_REGEX = re.compile(r"(@[^\s]+\s+)|(#(?=[^\s]+))")

    def __init__(self):
        # self.stemmer = PorterStemmer()
        self.stemmer = SnowballStemmer('english')
        self.tokenizer = TweetTokenizer()
        self.stopwords = StopWords.words('english')

    def get(self, sentence):
        detweeted = re.sub(self.TWITTER_REGEX, '', sentence)
        # detweeted = sentence
        expanded = Contractions.expand(detweeted.lower())
        tokens = self.tokenizer.tokenize(expanded)
        
        features = {}
        for token in tokens:
            if token not in self.stopwords:
                stemmed = self.stemmer.stem(token)
                features[f"w_{stemmed}"] = stemmed

        # for feature in cFeatures:
        #     if feature in expanded:
        #         features[cFeatures[feature]] = True

        return features