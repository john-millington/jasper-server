import sys
from corpus.SentimentFeatures import SentimentFeatures
from corpus.Corpus import Corpus

Loader = Corpus()
print(Loader.get(10, "acl-train"))

# FeatureRecognition = SentimentFeatures()
# Sentence = sys.argv[1]

# print(FeatureRecognition.get(Sentence))