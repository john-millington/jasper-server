import sys
from corpus.Features import Features

FeatureRecognition = Features()
Sentence = sys.argv[1]

print(FeatureRecognition.get(Sentence))