import argparse
import json
import pickle

from trainers.DynamoDBTester import DynamoDBTester

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--classifier', help='Path to the pickled classifier object')
parser.add_argument('-r', '--resource', help='Name of library to test against', default='sentiment')

args = parser.parse_args()
if args.classifier != None:
    file = open(args.classifier, 'rb')
    classifier = pickle.load(file)
    file.close()

    tester = DynamoDBTester(classifier = classifier, resource=args.resource, output='output.txt')
    results = tester.test()

    print(json.dumps(results, indent=4, sort_keys=True))