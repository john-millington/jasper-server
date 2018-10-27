import math
import random

from trainers.DynamoDBResource import DynamoDBResource
from corpus.SentimentFeatures import SentimentFeatures
from trainers.MultilayeredRecursiveRegression import MultilayeredRecursiveRegression

class DynamoDBTrainer(DynamoDBResource):
    def __init__(self, resource, trim = True, features = SentimentFeatures(), test_ratio = 0.3):
        self.trim = trim
        self.features = features
        self.test_ratio = test_ratio

        super().__init__(resource = resource)

        self.configure()

    
    def configure(self):
        resources = self.get_resources()
        resources.sort(key=lambda resource: resource['confidence'], reverse=True)

        features = self.get_features(resources)

        normalised = self.normalise(features)
        tests = self.get_tests(normalised)

        self.trainer = MultilayeredRecursiveRegression({
            "base_data": [],
            "block_size": 400,
            "feature_data": normalised,
            "test_data": tests,
            "thread_count": 1
        })


    def get_features(self, resources):
        features = []
        for resource in resources:
            text = resource['text']
            if ('full_text' in resource):
                text = resource['full_text']

            features.append([
                self.features.get(text),
                resource[self.resource]
            ])

        return features


    def get_groups(self, features):
        groups = {}
        for entry in features:
            if entry[1] not in groups:
                groups[entry[1]] = []

            groups[entry[1]].append(entry)

        return groups


    def get_tests(self, features):
        tests = []
        groups = self.get_groups(features)

        for group in groups:
            size = round(len(groups[group]) * self.test_ratio)
            tests = tests + groups[group][0:size]

        return tests


    def normalise(self, features):
        if not self.trim:
            return features

        groups = self.get_groups(features)
        
        threshold = math.inf
        for group in groups:
            if len(groups[group]) < threshold:
                threshold = len(groups[group])
            
            # random.shuffle(groups[group])
                
        
        rebased = []
        for group in groups:
            rebased = rebased + groups[group][0:threshold]


        random.shuffle(rebased)
        return rebased


    def train(self):
        return self.trainer.train()