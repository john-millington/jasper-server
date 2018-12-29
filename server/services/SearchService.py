import json
import sys
import os
import re
import pytextrank

from dateutil.parser import parse

from newsapi import NewsApiClient
from TwitterAPI import TwitterAPI

class SearchService:
    SOURCES_FILE = './server/services/data/sources.json'

    NEWS_LIMIT = 100
    TWITTER_LIMIT = 100

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


    def get_news(self, query, count):
        response = self.news_client.get_everything(
            q=query['q'][0],
            sources=self.get_source_list(),
            language='en',
            sort_by='publishedAt',
            page_size=int(count)
        )

        articles = []
        for article in response['articles']:
            parsed = parse(article['publishedAt'])

            formatted = parsed.isoformat()
            timestamp = int(parsed.timestamp())

            content = ''
            if article['title'] != None:
                content += article['title']

            if article['description'] != None:
                content += ' ' + article['description']

            articles.append({
                'source': article['source']['name'],
                'text': content,
                'meta': {
                    'type': 'search.news',
                    'source_url': article['url'],
                    'image_url': article['urlToImage'],
                    'created_at': formatted,
                    'timestamp': timestamp
                }
            })

        return articles

    
    def get_tweets(self, query, count):
        tweet_query = { 
            'q': query['q'][0] + ' -filter:retweets',
            'tweet_mode': 'extended',
            'count': count,
            'lang': 'en',
            'result_type': 'recent',
            'include_entities': 'false'
        }

        if ('order' in query):
            tweet_query['result_type'] = query['order']

        if ('until' in query):
            tweet_query['until'] = query['until']

        if ('since' in query):
            tweet_query['since_id'] = query['since']

        results = self.twitter_client.request('search/tweets', tweet_query)

        tweets = []
        for result in results:
            parsed = parse(result['created_at'])

            formatted = parsed.isoformat()
            timestamp = int(parsed.timestamp())

            tweets.append({
                'source': '@' + result['user']['screen_name'],
                'text': result['full_text'],
                'meta': {
                    'type': 'search.tweet',
                    'reply_to': result['in_reply_to_status_id_str'],
                    'created_at': formatted,
                    'timestamp': timestamp
                }
            })

        return tweets


    def handle(self, query, type):
        if 'q' in query:
            tweets = self.tweets(query)
            news = self.news(query)

            # themes = self.themes(tweets, news)
            response = {
                'tweets': tweets,
                'news': news
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
            count = int(query['count'][0])

        articles = []
        while (count > 0):
            actual_count = count
            if (actual_count > self.NEWS_LIMIT):
                actual_count = self.NEWS_LIMIT

            articles = articles + self.get_news(query, actual_count)
            count = count - self.NEWS_LIMIT

        return articles


    def themes(self, tweets, news):
        stage0 = 'stage0.json'
        stage1 = 'stage1.json'

        with open(stage0, 'w') as source:
            for tweet in tweets:
                tweet['id'] = tweet['meta']['timestamp']
                source.write(json.dumps(tweet))
                source.write('\n')

            for article in news:
                article['id'] = article['meta']['timestamp']
                source.write(json.dumps(article))
                source.write('\n')

        with open(stage1, 'w') as graph_output:
            for graf in pytextrank.parse_doc(pytextrank.json_iter(stage0)):
                graph_output.write("%s\n" % pytextrank.pretty_print(graf._asdict()))

        graph, ranks = pytextrank.text_rank(stage1)
        pytextrank.render_ranks(graph, ranks)

        themes = []
        for rl in pytextrank.normalize_key_phrases(stage1, ranks):
            themes.append(rl)

        os.remove(stage0)
        os.remove(stage1)

        return rl

    
    def tweets(self, query):
        count = 20
        if ('count' in query):
            count = int(query['count'][0])

        tweets = []
        while (count > 0):
            actual_count = count
            if (actual_count > self.TWITTER_LIMIT):
                actual_count = self.TWITTER_LIMIT

            tweets = tweets + self.get_tweets(query, actual_count)
            count = count - self.TWITTER_LIMIT

        return tweets