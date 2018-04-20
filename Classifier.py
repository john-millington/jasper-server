import pickle
import argparse

from corpus.Features import Features
from classifiers.Classifier import Classifier

class Classifier:
    PICKLE_PATH = './trainers/trained/acl-wiki-delta-range.pickle'

    def __init__(self):
        file = open(self.PICKLE_PATH, 'rb')
        self.classifier = pickle.load(file)
        file.close()

        self.features = Features()

    def classify(self, text):
        features = self.features.get(text)
        return self.classifier.classify(features)

    def prop_classify(self, text):
        features = self.features.get(text)
        return self.classifier.prob_classify(features)