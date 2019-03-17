from jane import EmotionClassifier
from jane import SentimentClassifier

class Classifier:
  def __init__(self):
    self.sentiment_classifier = SentimentClassifier()
    self.emotion_classifier = EmotionClassifier()


  def sentiment(self, text):
    return self.sentiment_classifier.prob_classify(text)

  
  def special(self, text):
    return self.emotion_classifier.prob_classify(text)
