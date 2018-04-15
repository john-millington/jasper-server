from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

from corpus.Contractions import Contractions

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
            features[stemmed] = stemmed

        return features