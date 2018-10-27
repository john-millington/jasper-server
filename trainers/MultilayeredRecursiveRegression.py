import math
import random

from trainers.ProbDist import ProbDist
from trainers.RecursiveRegressionClassifier import RecursiveRegressionClassifier
from trainers.RegressionType import RegressionType

class MultilayeredRecursiveRegression:
    def __init__(self, config):
        self.config = config

        self.feature_data = config['feature_data']
        self.test_data = config['test_data']

    
    def classify(self, features):
        return self.prob_classify(features).max()

    
    # TODO
    # TODO - This algorithm needs work, total bollocks
    # TODO
    def prob_classify(self, features):
        keys = sorted(self.classifiers.keys())
        results = [1] * len(keys)

        for (key_index, layer) in enumerate(keys):
            result = self.classifiers[layer].prob_classify(features)
            results[key_index] = result.prob(layer)

        for (index, value) in enumerate(results):
            results[index] = math.exp(value)
            
        totals = sum(results)
        for (index, value) in enumerate(results):
            results[index] = (value / totals)

        copied_results = results[:]
        max_result = max(copied_results)
        copied_results.remove(max_result)
        confidence = (max_result - max(copied_results))

        return ProbDist(dict(zip(keys, results)), confidence)

    
    def recast(self, type):
        return type(self.classifiers)

    
    def get_layers(self, feature_set):
        separated = {}
        for labeled_features in feature_set:
            label = labeled_features[1]
            if label not in separated:
                separated[label] = []

            separated[label].append(labeled_features)

        layers = {}
        label_count = len(separated.keys())
        for classification in separated:
            count = len(separated[classification])
            sample_size = round(count / (label_count - 1))

            samples = []
            for inner in separated:
                if inner != classification:
                    random.shuffle(separated[inner])
                    samples += separated[inner][0:sample_size]

            layer_features = self.untag(samples) + separated[classification]
            random.shuffle(layer_features)

            layers[classification] = {
                'count': len(layer_features),
                'feature_set': layer_features
            }

        return {
            'label_count': len(layers.keys()),
            'layers': layers
        }

    
    def train(self):
        layers = self.get_layers(self.feature_data)
        test_layers = self.get_layers(self.test_data)
        
        self.classifiers = {}
        self.results = {}
        for layer in layers['layers']:
            classifier = RecursiveRegressionClassifier({
                **self.config,
                'feature_data': layers['layers'][layer]['feature_set'],
                'test_data': test_layers['layers'][layer]['feature_set'],
                'regression_type': RegressionType.DELTA_RANGE,
                'name': layer
            })

            result = classifier.train()
            self.classifiers[layer] = result['classifier']

            del result['classifier']
            self.results[layer] = result

        self.results['classifier'] = self
        return self.results

    
    def untag(self, feature_set):
        copied = []
        for labeled_feature in feature_set:
            copied.append([labeled_feature[0], 'untagged_label'])

        return copied
        