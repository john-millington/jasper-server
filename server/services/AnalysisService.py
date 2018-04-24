import random

from server.core.Classifier import Classifier
from server.services.SearchService import SearchService

class AnalysisService(SearchService):
    def __init__(self):
        self.classifier = Classifier()
        super().__init__()


    def analyse(self, query):
        results = self.tweets(query) + self.news(query)
        sorted(results, key=lambda result: result['meta']['timestamp'])
        # random.shuffle(results)

        fields = []
        if ('fields' in query):
            fields = query['fields'][0].split(',')

        curated = []
        for result in results:
            text = result['text']

            sentiment = self.classifier.sentiment(text)
            special = self.classifier.special(text)

            sentiment_max = sentiment.max()
            special_max = special.max()

            if (sentiment_max == 'neutral'):
                if (special_max not in ['sadness', 'surprise', 'fear', 'joy']):
                    continue

            if (sentiment_max == 'positive'):
                if (special_max not in ['joy', 'love']):
                    continue

            if (sentiment_max == 'negative'):
                if (special_max not in ['anger', 'sadness']):
                    continue

            meta = result['meta']

            curation = {
                **result,
                'meta': {
                    **meta
                }
            }

            if ('sentiment' in fields):
                
                curation['sentiment'] = {
                    'sentiment': sentiment.max(),
                    'scores': sentiment.dict(),
                    'confidence': sentiment.confidence()
                }

            if ('language' in fields):
                language = self.classifier.language(text)
                curation['language'] = {
                    'code': language.max(),
                    'confidence': language.confidence()
                }

            if ('special' in fields):
                curation['special'] = {
                    'sentiment': special.max(),
                    'scores': special.dict(),
                    'confidence': special.confidence()
                }

            if ('structure' in fields):
                structure = self.classifier.structure(text)
                curation['structure'] = structure

            curated.append(curation)

        return {
            'results': curated
        }

    def handle(self, query):
        if 'q' in query:
            return self.analyse(query)
        
        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }