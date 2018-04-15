import sys
from corpus.Features import Features
from corpus.Corpus import Corpus

Loader = Corpus()
Loader.get(10000, "sentiment140")
print(Features.FOUND_FEATURES)

# FeatureRecognition = Features()
# Sentence = sys.argv[1]

# print(FeatureRecognition.get(Sentence))