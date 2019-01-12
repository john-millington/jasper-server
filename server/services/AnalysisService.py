import boto3
import random
import spacy

from corpus.KeyPhrase import KeyPhrase
from corpus.KeyPhrase2 import KeyPhrase2
from corpus.StringParser import StringParser
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


            if ('language' in fields):
                curation['language'] = self.classifier.language(text)


            if ('phrases' in fields):
                phrases = KeyPhrase2.extract(text)
                curation['phrases'] = phrases

            
            if ('perspective' in fields):
                parsed = self.nlp(result['text'])
                curation['perspective'] = self.get_perspective(parsed.print_tree(), 1, [])


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


            if ('structure' in fields):
                structure = self.classifier.structure(text)
                curation['structure'] = structure

            curated.append(curation)

        return {
            'count': len(curated),
            'results': curated
        }

    
    def get_perspective(self, tree, level, subjects):
        ignore = [
            'which',
            'that',
            'it',
            'they',
            'he',
            'one',
            'who',
            'she'
        ]

        for item in tree:
            if len(item['modifiers']) > 0:
                subject = self.get_perspective(item['modifiers'], level + 1, subjects)

            if item['arc'] == 'nsubj':
                if item['word'].lower() not in ignore:
                    subjects.append([item['word'], level])

        if (len(subjects)):
            reordered = sorted(subjects, key=lambda subject: subject[1], reverse=True)
            return reordered[0][0]

        return None


    def handle(self, query, type):
        if 'q' in query:
            fields = []
            if ('fields' in query):
                fields = query['fields'][0].split(',')

            response = self.analyse(query, fields)
            if ('topics' in query):
                count = int(query['topics'][0])
                response['topics'] = KeyPhrase2.topics(response['results'], count)

            # self.store(response, fields)
            return response
        
        return {
            'error': {
                'message': 'missing parameters',
                'code': 'JS_ERR_1000'
            }
        }

    
    def store(self, response, fields):
        dynamodb = boto3.resource('dynamodb')

        if ('emotion' in fields):
            emotion = dynamodb.Table('emotion')
            emotion_put = []

            with emotion.batch_writer() as batch:
                for result in response['results']:
                    if result['text'] in emotion_put:
                        continue

                    confidence = int(round(result['emotion']['confidence'], 2) * 100)
                    if confidence < 75:
                        continue

                    emotion_put.append(result['text'])

                    emotion_flag = result['emotion']['emotion']
                    score = int(round(result['emotion']['scores'][emotion_flag], 2) * 100)

                    batch.put_item(Item={
                        'text': result['text'],
                        'emotion': emotion_flag,
                        'score': score,
                        'confidence': confidence
                    })

        if ('sentiment' in fields):
            sentiment = dynamodb.Table('sentiment')
            sentiment_put = []

            with sentiment.batch_writer() as batch:
                for result in response['results']:
                    if result['text'] in sentiment_put:
                        continue

                    confidence = int(round(result['sentiment']['confidence'], 2) * 100)
                    if confidence < 70:
                        continue

                    sentiment_put.append(result['text'])

                    sentiment_flag = result['sentiment']['sentiment']
                    score = int(round(result['sentiment']['scores'][sentiment_flag], 2) * 100)

                    batch.put_item(Item={
                        'text': result['text'],
                        'sentiment': sentiment_flag,
                        'score': score,
                        'confidence': confidence
                    })