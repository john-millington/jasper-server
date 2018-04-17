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
    URLS_REGEX = re.compile(r"(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?\s?")

    def __init__(self):
        # self.stemmer = PorterStemmer()
        self.stemmer = SnowballStemmer('english')
        self.tokenizer = TweetTokenizer()
        self.stopwords = StopWords.words('english')

    def get(self, sentence):
        modified = re.sub(self.TWITTER_REGEX, '', sentence)
        modified = re.sub(self.URLS_REGEX, '', modified)
        expanded = Contractions.expand(modified.lower())
        tokens = self.tokenizer.tokenize(expanded)
        
        features = {}
        for token in tokens:
            if token not in self.stopwords:
                stemmed = self.stemmer.stem(token)
                features[f"w_{stemmed}"] = 1

        # for feature in cFeatures:
        #     if feature in expanded:
        #         features[cFeatures[feature]] = True

        return features