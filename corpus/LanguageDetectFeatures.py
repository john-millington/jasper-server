from nltk.tokenize import TreebankWordTokenizer
from corpus.Contractions import Contractions

class LanguageDetectFeatures:
    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()
    
    def get(self, sentence):
        expanded = Contractions.expand(sentence.lower())
        tokens = self.tokenizer.tokenize(expanded)
        
        features = {}
        for token in tokens:
            features[token] = 1

        return features