import time

from byron.storage.DynamoDBConnect import DynamoDBConnect
from corpus.SentimentFeatures import SentimentFeatures

class DynamoDBTester(DynamoDBConnect):
    def __init__(self, classifier, resource, features = SentimentFeatures(), output = None):
        self.classifier = classifier
        self.features = features
        self.output = output

        super().__init__(resource = resource)


    def get_features(self, resources):
        features = []
        for resource in resources:
            text = resource['text']
            if ('full_text' in resource):
                text = resource['full_text']

            features.append([
                self.features.get(text),
                resource[self.resource],
                text
            ])

        return features


    def test(self):
        resources = self.get_resources()
        features = self.get_features(resources)

        start_time = time.clock()
        total = 0
        incorrect = 0
        outcomes = {}
        classifications = {}
        lines = []

        line_format = '{:<20s}{:<20s}{:<500s}'

        for resource in features:
            feature_set = resource[0]
            classification = resource[1]

            result = self.classifier.prob_classify(feature_set)

            outcome = result.max()
            total += 1

            if classification not in classifications:
                classifications[classification] = 0

            if classification not in outcomes:
                outcomes[classification] = {}

            if outcome not in outcomes[classification]:
                outcomes[classification][outcome] = 0

            classifications[classification] += 1
            if (outcome != classification):
                outcomes[classification][outcome] += 1
                incorrect += 1

                if (self.output != None):
                    lines.append(line_format.format(outcome, classification, ' '.join(resource[2].split())))


        if (self.output != None):
            with open(self.output, 'a') as output:
                for line in lines:
                    output.write(line + '\n')


        accuracy = 1 - (float(incorrect) / total)
        time_taken = time.clock() - start_time
        ops_per_second = round(1 / (time_taken / total))

        return {
            'accuracy': accuracy * 100,
            'time': time_taken,
            'total_operations': total,
            'ops_per_second': ops_per_second,
            'outcomes': outcomes
        }