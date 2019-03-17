import random
import spacy

from corpus.KeyPhrase import KeyPhrase
from corpus.KeyPhrase2 import KeyPhrase2
from server.core.Classifier import Classifier
from server.services.SearchService import SearchService

class AnalysisService(SearchService):
    def __init__(self):
        self.classifier = Classifier()
        self.nlp = spacy.load('en')

        super().__init__()


    def analyse(self, query, fields):
        sources = ['twitter', 'news']
        if ('sources' in query):
            sources = query['sources'][0].split(',')

        results = []
        if ('twitter' in sources):
            results += self.tweets(query)

        if ('news' in sources):
            results += self.news(query)

        sorted(results, key=lambda result: result['meta']['timestamp'])
        # random.shuffle(results)

        curated = []
        for result in results:
            text = result['text']
            meta = result['meta']

            curation = {
                **result,
                'meta': {
                    **meta
                }
            }


            if ('phrases' in fields):
                phrases = KeyPhrase2.extract(text)
                curation['phrases'] = phrases

            
            if ('perspective' in fields):
                parsed = self.nlp(result['text'])
                curation['perspective'] = self.get_perspective(parsed.print_tree(), [])


            if ('sentiment' in fields):
                sentiment = self.classifier.sentiment(text)
                
                curation['sentiment'] = {
                    'sentiment': sentiment.max(),
                    'scores': sentiment.dict(),
                    'confidence': sentiment.confidence()
                }


            if ('emotion' in fields):
                emotion = self.classifier.special(text)
                emotion_type = emotion.max()
                confidence = emotion.confidence()

                if ('threshold' in query):
                    if confidence < (float(query['threshold'][0]) / 100):
                        emotion_type = 'neutral'
                        confidence = (float(query['threshold'][0]) / 100)


                curation['emotion'] = {
                    'emotion': emotion_type,
                    'scores': emotion.dict(),
                    'confidence': confidence
                }


            curated.append(curation)

        return {
            'count': len(curated),
            'results': curated
        }

    
    def get_perspective(self, tree, subjects = [], allow_modifiers = False, allow_preps = False):
        for item in tree:
            if allow_preps == False and item['arc'] == 'prep':
                continue

            elif item['arc'] == 'nsubj' or item['arc'] == 'dobj' or item['arc'] == 'pobj':
                if item['NE'] != '' and item['NE'] != 'DATE':
                    subjects.append(item['word'])

                    if len(item['modifiers']) > 0:
                        subjects = self.get_perspective(item['modifiers'], subjects, True, allow_preps)

                elif len(item['modifiers']) > 0:
                    subjects = self.get_perspective(item['modifiers'], subjects, True, allow_preps)


            elif allow_modifiers == True and item['arc'] == 'conj' or item['arc'] == 'appos':
                if item['NE'] != '' and item['NE'] != 'DATE':
                    subjects.append(item['word'])

                    if len(item['modifiers']) > 0:
                        subjects = self.get_perspective(item['modifiers'], subjects, True, allow_preps)
                
                    elif len(item['modifiers']) > 0:
                        subjects = self.get_perspective(item['modifiers'], subjects, True, allow_preps)


            elif len(item['modifiers']) > 0:
                subjects = self.get_perspective(item['modifiers'], subjects, False, allow_preps)

        
        if len(subjects) == 0 and allow_preps == False:
            subjects = self.get_perspective(tree, subjects, False, True)


        return subjects


    def handle(self, query, type):
        if 'q' in query:
            fields = []
            if ('fields' in query):
                fields = query['fields'][0].split(',')

            response = self.analyse(query, fields)
            if ('topics' in query):
                count = int(query['topics'][0])
                response['topics'] = KeyPhrase2.topics(response['results'], count)

            return response
        

        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }
