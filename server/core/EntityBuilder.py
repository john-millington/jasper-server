import json
import requests

from server.core.Entity import Entity

WIKI_DISCOVERY_ENDPOINT = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&format=json&languages=en'

class EntityBuilder:
  def __init__(self, entity):
    self.entity = entity

  
  def get(self):
    endpoint = WIKI_DISCOVERY_ENDPOINT.format(self.entity)
    response = requests.get(endpoint)

    parsed = response.json()

    response = {}
    if 'entities' in parsed and self.entity in parsed['entities']:
      entity_struct = Entity(parsed['entities'][self.entity])
      response = entity_struct.extract()

    return self.resolve(response)

  
  def resolve(self, result):
    ids = []

    for entity_property in result:
      if isinstance(result[entity_property], dict):
        if 'id' in result[entity_property]:
          ids.append(result[entity_property]['id'])
        else:
          for dict_item_name in result[entity_property]:
            dict_item = result[entity_property][dict_item_name]
            if isinstance(dict_item, dict):
              if 'id' in dict_item:
                ids.append(dict_item['id'])


      elif isinstance(result[entity_property], list):
        for list_item in result[entity_property]:
          if isinstance(list_item, dict):
            if 'id' in list_item:
              ids.append(list_item['id'])


    if (len(ids) > 0):
      references = {
        'entities': {}
      }

      for index, item in enumerate(ids):
        if (index % 50) > 0:
          continue

        ids_splice = ids[index:index + 50]
        endpoint = WIKI_DISCOVERY_ENDPOINT.format('|'.join(ids_splice)) + '&props=labels|descriptions'

        response = requests.get(endpoint)
        json_response = response.json()

        if 'entities' in json_response:
          references['entities'] = {
            **references['entities'],
            **json_response['entities']
          }


      if 'entities' in references:
        for reference_id in references['entities']:
          reference = Entity(references['entities'][reference_id])

          reference_value = {
            'title': reference.get_value('labels'),
            'description': reference.get_value('descriptions'),
            'id': reference_id
          }

          for entity_property in result:
            if isinstance(result[entity_property], dict):
              if 'id' in result[entity_property]:
                if result[entity_property]['id'] == reference_id:
                  result[entity_property] = reference_value
              else:
                for dict_item_name in result[entity_property]:
                  dict_item = result[entity_property][dict_item_name]
                  if isinstance(dict_item, dict):
                    if 'id' in dict_item and dict_item['id'] == reference_id:
                      result[entity_property][dict_item_name] = reference_value

            elif isinstance(result[entity_property], list):
              for index, list_item in enumerate(result[entity_property]):
                if isinstance(list_item, dict):
                  if 'id' in list_item and list_item['id'] == reference_id:
                    result[entity_property][index] = reference_value


    return result