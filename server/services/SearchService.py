from TwitterAPI import TwitterAPI

class SearchService:
    def __init__(self):
        self.client = TwitterAPI(
            os.environ.get('TWITTER_CONSUMER_KEY'),
            os.environ.get('TWITTER_CONSUMER_SECRET'),
            os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
            os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )

    def handle(self, query):
        if 'q' in query:
            response = {
                'tweets': [
                    
                ]
            }

            count = 20
            if ('count' in query):
                count = query['count'][0]

            results = self.client.request('search/tweets', { 
                'q': query['q'][0],
                'tweet_mode': 'extended',
                'exclude_retweets': True,
                'count': count
            })

            for result in results: 
                response['tweets'].append(result)

            return response
        
        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }