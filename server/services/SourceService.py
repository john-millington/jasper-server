import html2text
import requests
import nltk

from bs4 import BeautifulSoup, NavigableString, Tag

from server.core.Classifier import Classifier
from server.services.SearchService import SearchService

class SourceService(SearchService):
    def __init__(self):
        # self.classifier = Classifier()

        self.parser = html2text.HTML2Text()
        self.parser.ignore_links = True
        self.parser.ignore_images = True
        self.parser.ignore_tables = True

        super().__init__()

    
    def handle(self, query):
        if query['meta']['type'] == 'search.news':
            response = self.news(query)
        elif query['meta']['type'] == 'search.tweet':
            response = self.tweet(query)
        else:
            response = {
                'error': {
                    'message': 'unknow source type',
                    'code': 'JS_ERR_5000'
                }
            }

        return response

    
    def news(self, query):
        source = query['meta']['source_url']
        clean_text = requests.get(f'http://boilerpipe-web.appspot.com/extract?url={source}&extractor=ArticleExtractor&output=htmlFragment')

        return {
            'contents': [ 
                {
                    'text': clean_text.text,
                    'source': query['source'],
                    'meta': query['meta']
                }
            ]
        }


    def tweet(self, query):
        response = {
            'contents': [
                query
            ]
        }
        reply = query['meta']['reply_to']
        if (reply != None):
            result = self.twitter_client.request('statuses/show/:%s' % reply, {
                'tweet_mode': 'extended'
            })

            for tweet in result:
                response['contents'].append({
                    'text': tweet['full_text'],
                    'source': '@' + tweet['user']['screen_name'],
                    'meta': {
                        'type': 'search.tweet',
                        'reply_to': tweet['in_reply_to_status_id_str']
                    }
                })

        response['contents'].append(query)

        return response
        

