from TwitterAPI import TwitterAPI
from server.core.Classifier import Classifier

class AnalysisService:
    def __init__(self):
        self.classifier = Classifier()

        self.client = TwitterAPI(
            os.environ.get('TWITTER_CONSUMER_KEY'),
            os.environ.get('TWITTER_CONSUMER_SECRET'),
            os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
            os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )

    def analyse(self, query):
        count = 20
        if ('count' in query):
            count = query['count'][0]

        results = self.client.request('search/tweets', { 
            'q': query['q'][0] + ' -filter:retweets AND -filter:replies',
            'tweet_mode': 'extended',
            'count': count
        })

        fields = []
        if ('fields' in query):
            fields = query['fields'][0].split(',')

        curated = []
        for result in results:
            text = result['full_text']
            curation = { 
                'text': text
            }

            if ('sentiment' in fields):
                sentiment = self.classifier.sentiment(text)
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
                special = self.classifier.special(text)
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
            'tweets': curated
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