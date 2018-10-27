import argparse
import datetime
import json
import pickle
import time

from trainers.DynamoDBTrainer import DynamoDBTrainer

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='Name of the classifier - it will be saved to a file named the same under the trainers/trained path', required=True)
parser.add_argument('-r', '--resource', help='DB name to pull training set from', required=True)
args = parser.parse_args()

if args.name != None and args.resource != None:
    trainer = DynamoDBTrainer(resource=args.resource)

    start = time.time()
    result = trainer.train()
    end = time.time()

    if (result["classifier"] != None):
        output = open(f'trainers/trained/{args.name}.pickle', 'wb')
        pickle.dump(result["classifier"], output)
        output.close()

        del result['classifier']
        for classification in result:
            if 'set' in result[classification]:
                result[classification]['document_count'] = len(result[classification]['set'])
                del result[classification]['set']


        with open(f'trainers/trained/{args.name}.json', 'w') as jsonout:
            json.dump({
                'resource': args.resource,
                'classifier': f'{args.name}.pickle',
                'time': str(datetime.timedelta(seconds=end - start)),
                'statistics': result
            }, jsonout, indent=4, sort_keys=True)
