import ctypes

import boto3
import json

from time import time
from datetime import datetime
from newsapi import NewsApiClient

SOURCES_FILE = './server/services/data/sources.json'
SOURCES = json.load(open(SOURCES_FILE))

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('articles')

def get_source_list(lang = 'en'):
  source_list = []
  for source in SOURCES['sources']:
    if (source['language'] == lang):
      source_list.append(source['id'])

  return ','.join(source_list)

def get_news_articles(timestamp, count = 100, page = 1):
  news_client = NewsApiClient(api_key=os.environ.get('NEWS_CLIENT_API_KEY'))

  response = news_client.get_everything(
    q='',
    from_param=timestamp,
    language='en',
    page=int(page),
    page_size=int(count),
    sort_by='publishedAt',
    sources=get_source_list()
  )

  articles = response['articles']
  if response['totalResults'] > (count * page) and (count * page) < 1001:
    articles.extend(get_news_articles(timestamp, count, page + 1))


  return articles


def scrape(interval = 20):
  timestamp = datetime.fromtimestamp(time() - (interval * 60)).strftime('%Y-%m-%dT%H:%M:%S')
  articles = get_news_articles(timestamp)

  with table.batch_writer() as batch:
    for article in articles:
      try:
        id_value = ctypes.c_size_t(hash(article['title'])).value
        
        item = {
          **article,
          'id': str(id_value)
        }

        batch.put_item(Item = item)
      except:
        print(article)


scrape()
