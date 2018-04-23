from server.core.Classifier import Classifier

class ClassifyService:

    def __init__(self):
        self.classifier = Classifier()


    def classify(self, text):
        sentiment = self.classifier.sentiment(text)
        language = self.classifier.language(text)
        special = self.classifier.special(text)
        structure = self.classifier.structure(text)

        return {
            'text': text,
            'language': {
                'code': language.max(),
                'scores': language.dict(),
                'confidence': language.confidence()
            },
            'sentiment': {
                'sentiment': sentiment.max(),
                'scores': sentiment.dict(),
                'confidence': sentiment.confidence()
            },
            'special': {
                'sentiment': special.max(),
                'scores': special.dict(),
                'confidence': special.confidence()
            },
            'structure': structure
        }


    def handle(self, query):
        if 'text' in query:
            return self.classify(query['text'][0])

        if 'texts' in query:
            results = []
            for text in query['texts']:
                results.append(self.classify(text))

            return {
                'texts': results
            }

        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }