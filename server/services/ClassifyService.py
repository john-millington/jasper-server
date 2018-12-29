from server.core.Classifier import Classifier

class ClassifyService:

    def __init__(self):
        self.classifier = Classifier()


    def classify(self, text, fields):
        response = {
            'text': text
        }

        if 'sentiment' in fields:
            sentiment = self.classifier.sentiment(text)

            response['sentiment'] = {
                'sentiment': sentiment.max(),
                'scores': sentiment.dict(),
                'confidence': sentiment.confidence()
            }


        if 'language' in fields:
            response['language'] = self.classifier.language(text)


        if 'special' in fields:
            special = self.classifier.special(text)

            response['special'] = {
                'sentiment': special.max(),
                'scores': special.dict(),
                'confidence': special.confidence()
            }


        if 'structure' in fields:
            response['structure'] = self.classifier.structure(text)


        return response


    def handle(self, query, type):
        fields = []
        if ('fields' in query):
            fields = query['fields'][0].split(',')

        if 'text' in query:
            return self.classify(query['text'][0], fields)

        if 'texts' in query:
            results = []
            for text in query['texts']:
                results.append(self.classify(text), fields)

            return {
                'texts': results
            }

        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }