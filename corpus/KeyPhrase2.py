from nltk.corpus import stopwords as StopWords
import spacy

class KeyPhrase2:
  NLP = spacy.load('en')
  STOPWORDS = StopWords.words('english')

  @staticmethod
  def extract(text):
    doc = KeyPhrase2.NLP(text)
    
    nouns = []
    for noun in doc.noun_chunks:
      text = []

      for word in noun.text.split(' '):
        if word not in KeyPhrase2.STOPWORDS:
          text.append(word)

      nouns.append(' '.join(text))

    return nouns


  @staticmethod
  def topics(results, count = 5, radius = 5):
    topics = {}
    linked_topics = {}

    for result in results:
      words = result['text'].split(' ')
      for (index, word) in enumerate(words):
        if word.lower() in KeyPhrase2.STOPWORDS or len(word) == 0 or word[0].isupper() != True:
          continue

        phrase = ''
        extension = 0

        phrases = []
        while extension < radius and len(words) > (index + extension):
          phrase = (phrase + ' ' + words[(index + extension)]).strip()
          phrases.append(phrase)

          if phrase not in topics:
            topics[phrase] = {
              'count': 0,
              'linked': [],
              'phrase': phrase,
              'score': 0
            }

          extension = extension + 1

          topics[phrase]['count'] = topics[phrase]['count'] + 1
          topics[phrase]['linked'].append(result)
          topics[phrase]['score'] = topics[phrase]['score'] + extension

        for phrase in phrases:
          copy = phrases.copy()
          copy.remove(phrase)

          if phrase not in linked_topics:
            linked_topics[phrase] = []

          linked_topics[phrase].extend(copy)


    resorted = sorted(topics.values(), key=lambda topic: topic['score'], reverse=True)

    for (index, resolved) in enumerate(resorted):
      topics = linked_topics[resolved['phrase']]
      
      iteration_index = index + 1
      while iteration_index < len(resorted):
        inner_phrase = resorted[iteration_index]['phrase']
        
        is_duplicate = inner_phrase in topics
        # if is_duplicate != True:
        #   is_duplicate = inner_phrase in resolved['phrase'] or resolved['phrase'] in inner_phrase

        if is_duplicate == True:
          duplicate = resorted[iteration_index]

          for linked in duplicate['linked']:
            if linked not in resolved['linked']:
              # resolved['linked'].append(linked)
              resolved['count'] = resolved['count'] + 1
              resolved['score'] = resolved['score'] + len(inner_phrase.split(' '))
          
          resorted.remove(duplicate)
          linked_topics[resolved['phrase']].extend(linked_topics[duplicate['phrase']])

        else:
          iteration_index = iteration_index + 1


    preprocessed = sorted(resorted, key=lambda topic: topic['score'], reverse=True)[0:count]
    for resolved in preprocessed:
      for linked in resolved['linked']:
        if 'topics' not in linked:
          linked['topics'] = []

        if resolved['phrase'] not in linked['topics']:
          linked['topics'].append(resolved['phrase'])

      resolved['linked'] = None

    return preprocessed
    
    
