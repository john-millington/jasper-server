import re

from nltk.tokenize import TreebankWordTokenizer
from corpus.Contractions import Contractions

class LanguageDetectFeatures:
    NUMBER_REGEX = re.compile(r'[0-9]+((\.|\,){1}[0-9]+)?((\.|\,){1}[0-9]+)?')
    URLS_REGEX = re.compile(r"(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?\s?")

    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()
    
    def get(self, sentence):
        modified = re.sub(self.NUMBER_REGEX, '', sentence)
        modified = re.sub(self.URLS_REGEX, '', modified)
        
        expanded = Contractions.expand(modified.lower())
        tokens = self.tokenizer.tokenize(expanded)
        
        features = {}
        for token in tokens:
            if len(token) < 2:
                continue

            features['w_' + token] = 1

        # for char in expanded:
        #     features['c_' + char] = 1

        return features