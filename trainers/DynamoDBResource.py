import boto3

class DynamoDBResource:
    def __init__(self, resource):
        self.resource = resource

        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.resource)

    
    def get_resources(self):
        results = self.table.scan()
        resources = results['Items']

        while 'LastEvaluatedKey' in results:
            results = self.table.scan(ExclusiveStartKey=results['LastEvaluatedKey'])
            resources = resources + results['Items']

        return resources