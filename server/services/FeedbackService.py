import boto3

class FeedbackService:
  def handle(self, query, type):
    dynamodb = boto3.resource('dynamodb')
    feedback = dynamodb.Table('feedback')

    feedback.put_item(Item={
      'feedback': query['feedback'],
      'original_classification': query['original_classification'],
      'text': query['text']
    })

    return {
      'success': True
    }