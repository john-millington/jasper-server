import requests
import nltk
import json
import urllib.parse

from server.core.Classifier import Classifier
from server.services.SearchService import SearchService

class SourceService(SearchService):
    def __init__(self):
        # self.classifier = Classifier()

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
        source_encode = urllib.parse.quote(source, safe='')
        clean_text = requests.get('http://boilerpipe-web.appspot.com/extract?url={}&extractor=ArticleExtractor&output=json'.format(source_encode))
        json_dump = clean_text.json()

        text = json_dump['response']['content']
        text_split = text.split('\n')
        for (index, item) in enumerate(text_split):
            text_split[index] = '<p class="result-view__paragraph">{}</p>'.format(item)

        formatted = ''.join(text_split)

        return {
            'contents': [ 
                {
                    'title': json_dump['response']['title'],
                    'text': formatted,
                    'source': query['source'],
                    'meta': query['meta']
                }
            ]
        }


    def tweet(self, query):
        response = {
            'contents': [ ]
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
        

