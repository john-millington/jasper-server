import pickle
from corpus.Features import Features

class Classifier:
  NEUTRAL_THRESHOLD = 0.2

  def __init__(self, classifier):
    pre_pickled = open(classifier, 'rb')
    self.classifier = pickle.load(pre_pickled)
    pre_pickled.close()

    self.features = Features()

  def classify(self, text):
    features = self.features.get(text)
    probabilities = self.classifier.prob_classify(features)

    pos = probabilities.prob('positive')
    neg = probabilities.prob('negative')

    neutral = 1 - abs(pos - neg)
    total = pos + neg + neutral

    pos = pos / total
    neg = neg / total
    neutral = neutral / total

    sentiment = 'positive'
    if neg > pos and neg > neutral:
      sentiment = 'negative'
    elif neutral > pos and neutral > neg:
      sentiment = 'neutral'

    return {
      "sentiment": sentiment,
      "scores": {
        "negative": neg,
        "positive": pos,
        "neutral": neutral
      }
    }    

