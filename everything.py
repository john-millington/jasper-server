import nltk
import pickle

from corpus.Corpus import Corpus

Loader = Corpus()
# sentiment140 = Loader.get(1600000, 'sentiment140')
acl = Loader.get(50000, 'acl-train')
wiki = Loader.get(25000, 'wiki-neutrals-train')
# reviews = Loader.get(3000, 'reviews')
# tweets = Loader.get(20000, 'twitter-sentiment-train')
# airline = Loader.get(20000, 'airline')

train_set = acl + wiki
classifier = nltk.NaiveBayesClassifier.train(train_set)

output = open(f'trainers/trained/everything-neutrals.pickle', 'wb')
pickle.dump(classifier, output)
output.close()