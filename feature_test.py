import sys
from corpus.Features import Features
from corpus.Corpus import Corpus

Loader = Corpus()
print(Loader.get(10, "acl-train"))

# FeatureRecognition = Features()
# Sentence = sys.argv[1]

# print(FeatureRecognition.get(Sentence))