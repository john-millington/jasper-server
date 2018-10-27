import boto3
import json
import time

class DynamoTransfer:
    def __init__(self, source, resource, selections):
        self.source = source
        self.resource = resource
        self.selections = selections

        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.resource)


    def begin(self):
        info = json.load(open('./corpus/data/{}/info.json'.format(self.source)))

        for classification in info['chunks']:
            max_chunks = info["chunks"][classification]
            if (self.selections != None):
                if (classification not in self.selections):
                    continue

            processed = []
            for x in range(1, max_chunks + 1):
                data = json.load(open('./corpus/data/{}/chunks/{}.chunk{}.json'.format(self.source, classification, x)))

                print('Processing chunk {} of {} for {}'.format(x, max_chunks, classification))                
                with self.table.batch_writer() as batch:
                    for line in data['lines']:
                        if (line['value'][0:400] in processed):
                            continue

                        batch.put_item(Item = {
                            'text': line['value'][0:400],
                            '{}'.format(self.resource): line['classification'],
                            'confidence': 1,
                            'source': self.source,
                            'full_text': line['value']
                        })

                        processed.append(line['value'][0:400])

                print("Waiting")
                time.sleep(10)
