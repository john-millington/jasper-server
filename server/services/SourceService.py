from server.services.SearchService import SearchService
from newspaper import Article

IGNORE = [
  'Join Independent Minds',
  'Shape Created with Sketch'
]

class SourceService(SearchService):
  def handle(self, query, type):
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

    parsed = Article(source)
    parsed.download()
    parsed.parse()

    text = parsed.text
    text_split = text.split('\n')
    for (index, item) in enumerate(text_split):
      should_ignore = False
      for (ignore_index, ignore) in enumerate(IGNORE):
        if item.startswith(ignore):
          should_ignore = True

      if (should_ignore):
        text_split[index] = ''
      else:
        text_split[index] = '<p class="result-view__paragraph">{}</p>'.format(item)

    formatted = ''.join(text_split)

    return {
      'contents': [ 
        {
          'title': parsed.title,
          'text': formatted,
          'source': query['source'],
          'meta': {
            **query['meta'],
            'authors': parsed.authors
          }
        }
      ]
    }


  def tweet(self, query):
    response = {
      'contents': [ ]
    }

    reply = query['meta']['reply_to']
    while (reply != None):
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

      reply = tweet['in_reply_to_status_id_str']

    response['contents'].reverse()
    response['contents'].append(query)

    return response
        

