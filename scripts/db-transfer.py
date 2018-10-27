import argparse
import json
import pickle

from corpus.DynamoTransfer import DynamoTransfer

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='Name of the library data to transfer')
parser.add_argument('-r', '--resource', help='Name of dynamo db resource to transfer to')
parser.add_argument('-t', '--types', help='Comma separated string of types to transfer')

args = parser.parse_args()
if args.source != None and args.resource != None:
    types = None
    if (args.types != None):
        types = args.types.split(',')

    transfer = DynamoTransfer(args.source, args.resource, types)
    transfer.begin()