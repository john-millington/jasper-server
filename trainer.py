import pickle
import time
import argparse

from corpus.Corpus import Corpus
from trainers.RecursiveRegressionClassifier import RecursiveRegressionClassifier

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='Name of the classifier - it will saved to a file named the same under the trainers/trained path', required=True)
parser.add_argument('-l', '--library', help='Name of the library to train against', default='sentiment140')
parser.add_argument('-s', '--size', help='Size of sample to train against', default=10000, type=int)
parser.add_argument('-b', '--block', help='Size of block to add in each iteration', default=100, type=int)
parser.add_argument('-t', '--threads', help='Number of threads to run the training algorithm in', default=1, type=int)

args = parser.parse_args()

if args.name != None:
  Loader = Corpus()
  start = time.time()

  Classifier = RecursiveRegressionClassifier({
      "base_data": [],
      "block_size": args.block,
      "feature_data": Loader.get(args.size, args.library),
      "test_data": Loader.get(3000, "reviews") + Loader.get(300, "tweets"),
      "thread_count": args.threads
  })

  result = Classifier.train()
  end = time.time()

  print (end - start)
  if (result["classifier"] != None):
      output = open(f'trainers/trained/{args.name}.pickle', 'wb')
      pickle.dump(result["classifier"], output)
      output.close()