import pickle
import argparse

from nltk.tree import Tree
from pycorenlp import StanfordCoreNLP

from corpus.SentimentFeatures import SentimentFeatures
from corpus.LanguageDetectFeatures import LanguageDetectFeatures
from classifiers.Classifier import Classifier

class Classifier:
    PICKLE_SENTIMENT_PATH = './classifiers/pickled/sentiment-classifier.pickle'
    # PICKLE_LANGUAGE_PATH = './classifiers/pickled/language-classifier.pickle'
    PICKLE_LANGUAGE_PATH = './classifiers/pickled/languages-trained.pickle'
    PICKLE_SPECIAL_PATH = './classifiers/pickled/special-classifier.pickle'

    def __init__(self):
        sentiment_file = open(self.PICKLE_SENTIMENT_PATH, 'rb')
        self.sentiment_classifier = pickle.load(sentiment_file)
        sentiment_file.close()

        language_file = open(self.PICKLE_LANGUAGE_PATH, 'rb')
        self.language_classifier = pickle.load(language_file)
        language_file.close()

        special_file = open(self.PICKLE_SPECIAL_PATH, 'rb')
        self.special_classifier = pickle.load(special_file)
        special_file.close()

        self.sentiment_features = SentimentFeatures()
        self.language_features = LanguageDetectFeatures()
        self.nlp = StanfordCoreNLP('http://localhost:9000')

    def language(self, text):
        features = self.language_features.get(text)
        return self.language_classifier.get(features)

    def sentiment(self, text):
        features = self.sentiment_features.get(text)
        return self.sentiment_classifier.prob_classify(features)

    def special(self, text):
        if (self.special_classifier != None):
            features = self.sentiment_features.get(text)
            return self.special_classifier.prob_classify(features)
        
        return None

    def structure(self, text):
        annotated = self.nlp.annotate(text, properties={
            'annotators': 'parse',
            'outputFormat': 'json'
        })

        results = []
        for sentence in annotated['sentences']:
            tree = Tree.fromstring(sentence['parse'])
            tree_string = ' '.join(tree.leaves())
            
            sentiment = self.sentiment(tree_string)
            special = self.special(tree_string)

            nounphrase = None
            verbphrase = None

            for subtree in tree[0]:
                if subtree.label() == 'NP':
                    nounphrase = ' ' .join(subtree.leaves())

                if (subtree.label() == 'VP'):
                    verbphrase = ' '.join(subtree.leaves())

            results.append({
                'text': tree_string,
                'subject': nounphrase,
                'descriptor': verbphrase,
                'sentiment': {
                    'sentiment': sentiment.max(),
                    'scores': sentiment.dict(),
                    'confidence': sentiment.confidence()
                },
                'special': {
                    'sentiment': special.max(),
                    'scores': special.dict(),
                    'confidence': special.confidence()
                }
            })

        return results
