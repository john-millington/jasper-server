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

    def prob_classify(self, features):
        results = [1] * len(sorted(self.classifiers.keys()))

        current_index = 0
        for layer in sorted(self.classifiers):
            result = self.classifiers[layer].prob_classify(features)

            untagged = result.prob('untagged_label')
            for_layer = result.prob(layer)

            polarity = for_layer - untagged

            inner_index = 0
            for value in results:
                if inner_index == current_index:
                    # results[inner_index] = max(0.01, result.prob(layer) + polarity)
                    results[inner_index] = (value + (result.prob(layer) * len(results)))
                else:
                    results[inner_index] = (value + result.prob('untagged_label'))

                inner_index += 1
                    
            current_index += 1

        totals = sum(results)
        for index, value in enumerate(results):
            results[index] = (value / totals) * 1

        return ProbDist(dict(zip(sorted(self.classifiers.keys()), results)))

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
        