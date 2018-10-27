import json

from nltk.corpus import stopwords as StopWords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer

from corpus.StringParser import StringParser

cFeatures = json.load(open('./corpus/data/features.json'))

class SentimentFeatures:
    def __init__(self):
        # self.stemmer = PorterStemmer()
        self.stemmer = SnowballStemmer('english')
        self.tokenizer = TweetTokenizer()
        self.stopwords = StopWords.words('english')

    def get(self, sentence):
        features = {}
        if sentence != None:
            tokens = StringParser.parse(sentence)
            
            for token in tokens:
                if len(token) > 1:
                    word_tag = 'w_{}'.format(token)
                    if word_tag in features:
                        word_tag = 'r_{}'.format(token)

                    features[word_tag] = 1

            # for feature in cFeatures:
            #     if feature in expanded:
            #         features[cFeatures[feature]] = 1

        return features