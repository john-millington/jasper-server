import requests
from server.core.EntityBuilder import EntityBuilder

WIKI_SEARCH_ENDPOINT = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&language=en&format=json&limit=10'

class EntityService:
  def get_entity_discovery(self, entity):
    entity_builder = EntityBuilder(entity)
    return entity_builder.get()


  def get_entities(self, query):
    endpoint = WIKI_SEARCH_ENDPOINT.format(query)
    response = requests.get(endpoint)

    parsed = response.json()
    
    count = 0
    results = None

    if 'search' in parsed:
      results = [self.result(result) for result in parsed['search']]
      count = len(results)

    return {
      'count': count,
      'results': results
    }

  
  def handle(self, query):
    if 'q' in query:
      return self.get_entities(query['q'][0])

    if 'entity' in query:
      return self.get_entity_discovery(query['entity'][0])

    return {
      'error': {
        'message': 'missing parameters',
        'code': 'JS_ERR_1000'
      }
    }

  
  def result(self, response):
    description = None
    if 'description' in response:
      description = response['description']

    return {
      'description': description,
      'id': response['id'],
      'title': response['label']
    }