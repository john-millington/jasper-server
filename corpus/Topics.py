import fuzzy
from corpus.KeyPhrase import KeyPhrase

class Topics:
    SOUNDEX = fuzzy.Soundex(4)

    @staticmethod
    def analyse(texts, count = 5, ignore = []):
        topics = {}
        for item in texts:
            phrases = KeyPhrase.extract(item['text'])
            for phrase in phrases:
                if phrase not in topics:
                    topics[phrase] = 0

                if phrase not in ignore:
                    topics[phrase] = topics[phrase] + 1

        recast = []
        for topic in topics:
            recast.append({
                'topic': topic,
                'count': topics[topic]
            })

        return sorted(Topics.dedupe(recast), key=lambda topic: topic['count'], reverse=True)[0:count]


    @staticmethod
    def dedupe(topics):
        for outer in topics:
            for inner in topics:
                if inner['count'] > 0:
                    if (inner != outer):
                        if Topics.SOUNDEX(inner['topic'].encode('utf8')) == Topics.SOUNDEX(outer['topic'].encode('utf8')):
                            if inner['count'] > outer['count']:
                                inner['count'] = inner['count'] + outer['count']
                                outer['count'] = -500
                            else:
                                outer['count'] = inner['count'] + outer['count']
                                inner['count'] = -500
        
        return [topic for topic in topics if topic['count'] > -1]


        
                