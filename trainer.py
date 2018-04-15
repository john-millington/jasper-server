import pickle
import time

from corpus.Corpus import Corpus
from trainers.RecursiveRegressionClassifier import RecursiveRegressionClassifier

Loader = Corpus()
start = time.time()

Classifier = RecursiveRegressionClassifier({
    "base_data": [],
    "block_size": 20,
    "feature_data": Loader.get(20, "sentiment140"),
    "test_data": Loader.get(20, "reviews") + Loader.get(20, "tweets"),
    "thread_count": 1
})

result = Classifier.train()
end = time.time()

print (end - start)
if (result["classifier"] != None):
    output = open('trainers/trained/recursive-regression-classifier-threaded.pickle', 'wb')
    pickle.dump(result["classifier"], output)
    output.close()