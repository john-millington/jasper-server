import json

from newsapi import NewsApiClient
from TwitterAPI import TwitterAPI

class SearchService:
    SOURCES_FILE = './server/services/data/sources.json'

    def __init__(self):
        self.twitter_client = TwitterAPI(
            os.environ.get('TWITTER_CONSUMER_KEY'),
            os.environ.get('TWITTER_CONSUMER_SECRET'),
            os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
            os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )

        self.news_client = NewsApiClient(api_key=os.environ.get('NEWS_CLIENT_API_KEY'))
        self.sources = json.load(open(self.SOURCES_FILE))


    def get_source_list(self, lang = 'en'):
        sources = []
        for source in self.sources['sources']:
            if (source['language'] == lang):
                sources.append(source['id'])

        return ','.join(sources)


    def handle(self, query):
        if 'q' in query:
            response = {
                'tweets': self.tweets(query),
                'news': self.news(query)
            }

            return response
        
        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }

    
    def news(self, query):
        count = 20
        if ('count' in query):
            count = query['count'][0]

        response = self.news_client.get_everything(
            q=query['q'][0],
            sources=self.get_source_list(),
            language='en',
            sort_by='relevancy',
            page_size=int(count)
        )

        articles = []
        for article in response['articles']:
            articles.append({
                'source': article['source']['name'],
                'text': article['title'],
                'meta': {
                    'type': 'search.news',
                    'source_url': article['url'],
                    'image_url': article['urlToImage']
                }
            })

            articles.append({
                'source': article['source']['name'],
                'text': article['description'],
                'meta': {
                    'type': 'search.news',
                    'source_url': article['url'],
                    'image_url': article['urlToImage']
                }
            })

        return articles

    
    def tweets(self, query):
        count = 20
        if ('count' in query):
            count = query['count'][0]

        results = self.twitter_client.request('search/tweets', { 
            'q': query['q'][0] + ' -filter:retweets',
            'tweet_mode': 'extended',
            'count': count,
            'lang': 'en',
            'result_type': 'recent',
            'include_entities': 'false'
        })

        tweets = []
        for result in results: 
            tweets.append({
                'source': '@' + result['user']['screen_name'],
                'text': result['full_text'],
                'meta': {
                    'type': 'search.tweet',
                    'reply_to': result['in_reply_to_status_id_str']
                }
            })

        return tweets