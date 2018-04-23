import math
import os
import random

from multiprocessing import Pool
from trainers.RegressionClassifier import RegressionClassifier

class RecursiveRegressionClassifier:
    def __init__(self, config):
        self.config = config

        self.base_data = []
        self.block_size = config["block_size"]
        self.feature_data = config["feature_data"]
        self.test_data = config["test_data"]
        self.thread_count = config["thread_count"]
        self.iterations = 0
        self.blocks = self.chunks(self.feature_data, self.thread_count)

        self.best = { "score": 0 }
    
    def chunks(self, target, chunks):
        chunk_size = math.ceil(len(target) / float(chunks))
        return [target[i:i + chunk_size] for i in range(0, len(target), chunk_size)]

    def thread(self, feature_data):
        classifier = RegressionClassifier({
            **self.config,
            "feature_data": feature_data,
            "base_data": self.base_data
        })

        return classifier.train()

    def train(self):
        self.iterations += 1

        results = None
        with Pool(len(self.blocks)) as pool:
            results = pool.map(self.thread, self.blocks)

        best = self.best
        for result in results:
            if (result["score"] > best["score"]):
                best = result

        os.system('clear')
        print("Iterations: {}".format(self.iterations))
        print("Score: {}".format(best["score"]))
        print("Best Score: {}".format(best["score"]))

        if (best["score"] > self.best["score"]):
            self.best = best
            self.base_data = best['set']
            
            random.shuffle(self.blocks)
            return self.train()

        self.best['iterations'] = self.iterations
        return self.best
