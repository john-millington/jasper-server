from datetime import datetime
from dateutil.parser import parse
from enum import Enum

import hashlib

WIKI_THUMB_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/{}/{}/{}/300px-{}'
WIKI_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/{}/{}/{}'

class EntityQualifierType(Enum):
  CURRENT = 1
  ALL = 2
  RECENT = 3


class Entity:
  SIMPLE_CLAIMS = {
    'singulars': {
      'twitter': 'P2002',
      'facebook': 'P2013',
      'instagram': 'P2003',
      'youtube': 'P2397',
      'linkedin': 'P4264',
      'website': 'P856',
      'blog': 'P1581',
      'gender': 'P21',
      'chief_executive': 'P169',
      'founded': 'P571',
      'date_of_birth': 'P569',
      'place_of_birth': 'P19',
      'spouse': 'P26',
      'political_party': 'P102'
    },
    'plurals': {
      'board': 'P3320',
      'related_entities': 'P463',
      'residency': 'P551',
      'industries': 'P452',
      'country': 'P17',
      'subsidiaries': 'P355',
      'headquarters': 'P159',
      'citizenship': 'P27',
      'positions_held': 'P39',
      'employer': 'P108',
      'products': 'P1056'
    }
  }

  def __init__(self, entity, qualifier = EntityQualifierType.CURRENT):
    self.entity = entity
    self.qualifier = qualifier

  
  def extract(self):
    extracted = {
      'id': self.entity['id'],
      'title': self.get_value('labels'),
      'description': self.get_value('descriptions'),
      'aliases': self.get_values('aliases'),
      'image': self.get_image()
    }

    singulars = Entity.SIMPLE_CLAIMS['singulars']
    for claim in singulars:
      claim_value = self.get_claim_value(singulars[claim])
      if claim_value != None:
        extracted[claim] = claim_value

    plurals = Entity.SIMPLE_CLAIMS['plurals']
    for claim in plurals:
      claims_values = self.get_claims_values(plurals[claim])
      if claims_values != None and len(claims_values) > 0:
        extracted[claim] = claims_values

    return extracted


  def get_claim(self, prop):
    claims = self.get_claims(prop)
    if len(claims) > 0:
      return claims[0]

    return None

  
  def get_claim_value(self, prop):
    claim_value = None

    claim = self.get_claim(prop)
    if claim != None and 'value' in claim:
      claim_value = claim['value']

    return claim_value


  def get_claims_values(self, prop):
    claims_values = None

    claims = self.get_claims(prop)
    if claims != None:
      claims_values = []
      for claim in claims:
        if 'value' in claim:
          claims_values.append(claim['value'])

    return claims_values


  def get_claims(self, prop):
    values = []
    if 'claims' in self.entity and prop in self.entity['claims']:
      claims = self.entity['claims'][prop]
      for claim in claims:
        if (self.qualify(claim)):
          if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
            values.append(claim['mainsnak']['datavalue'])

    return values


  def get_image(self):
    image = None

    claim = self.get_preferred_claim(['P154', 'P41', 'P94', 'P18'])
    if claim != None and 'value' in claim:
      found = claim['value']
      
      image_name = found['value'].replace(' ', '_')
      image_hash = hashlib.md5(image_name.encode('utf-8')).hexdigest()

      image_path = WIKI_THUMB_URL
      if claim['prop'] == 'P154':
        image_path = WIKI_IMAGE_URL

      image = image_path.format(
        image_hash[0],
        ''.join([image_hash[0], image_hash[1]]),
        image_name,
        image_name
      )

    return image


  def get_preferred_claim(self, order):
    claim_value = None
    for prop in order:
      claim = self.get_claim(prop)
      if claim != None:
        claim_value = {
          'prop': prop,
          'value': claim
        }

        break

    return claim_value


  def get_value(self, prop, lang = 'en'):
    values = self.get_values(prop, lang)
    if values != None and len(values) > 0:
      return values[0]

    return None


  def get_values(self, prop, lang = 'en'):
    values = None
    
    if prop in self.entity and lang in self.entity[prop]:
      properties = self.entity[prop][lang]
      values = []

      if isinstance(properties, list):
        for value in properties:
          if 'value' in value:
            values.append(value['value'])
      else:
        values.append(properties['value'])

    return values


  def qualify(self, claim):
    qualified = True

    if self.qualifier == EntityQualifierType.CURRENT:
      if 'qualifiers' in claim:
        if 'P580' in claim['qualifiers']:
          try:
            start_time_qualifier = claim['qualifiers']['P580'][0]
            start_time = parse(start_time_qualifier['datavalue']['value']['time'][1:])

            qualified = datetime.now().timestamp() > start_time.timestamp()
          except:
            pass


        if qualified and 'P582' in claim['qualifiers']:
          try:
            end_time_qualifier = claim['qualifiers']['P582'][0]
            end_time = parse(end_time_qualifier['datavalue']['value']['time'][1:])

            qualified = datetime.now().timestamp() < end_time.timestamp()
          except:
            pass


    return qualified