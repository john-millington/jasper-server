import random

from server.core.Classifier import Classifier
from server.services.SearchService import SearchService

class AnalysisService(SearchService):
    def __init__(self):
        self.classifier = Classifier()
        super().__init__()


    def analyse(self, query):
        sources = ['twitter', 'news']
        if ('sources' in query):
            sources = query['sources'][0].split(',')

        results = []
        if ('twitter' in sources):
            results += self.tweets(query)

        if ('news' in sources):
            results += self.news(query)

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

            meta = result['meta']

            curation = {
                **result,
                'meta': {
                    **meta
                }
            }

            sarcasm = False
            # if (sentiment_max == 'positive'):
            #     if (special_max in ['anger', 'sadness']):
            #         sarcasm = True

            # if (sentiment_max == 'negative'):
            #     if (special_max in ['love', 'joy']):
            #         sarcasm = True

            # curation['sarcasm'] = {
            #     'sarcasm': sarcasm,
            #     'confidence': (sentiment.confidence() + special.confidence()) / 2
            # }

            if ('language' in fields):
                language = self.classifier.language(text)
                curation['language'] = {
                    'code': language.max(),
                    'confidence': language.confidence()
                }

            if (sarcasm == False):
                if ('sentiment' in fields):    
                    curation['sentiment'] = {
                        'sentiment': sentiment.max(),
                        'scores': sentiment.dict(),
                        'confidence': sentiment.confidence()
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