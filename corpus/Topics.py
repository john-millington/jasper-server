import fuzzy
from corpus.KeyPhrase import KeyPhrase

class Topics:
    SOUNDEX = fuzzy.Soundex(4)

    @staticmethod
    def analyse(texts, count = 5, ignore = []):
        topics = []
        for item in texts:
            for phrase in item['phrases']:
                if phrase not in topics:
                    topics.append(phrase)
        

        revised = {}
        for outer_topic in topics:
            for inner_topic in topics:
                similarity = Topics.similarity(outer_topic, inner_topic)
                if (similarity['score'] > 0):
                    if inner_topic not in revised:
                        revised[inner_topic] = []

                    revised[inner_topic].append(similarity)

        for topic in revised:
            results = revised[topic]

            best = { 'score': 0.0 }
            for similarity in results:
                if similarity['score'] > best['score']:
                    best = similarity

            revised[topic] = best

        final_topics = []
        for topic in revised:
            final_topics.append(revised[topic]['text'])

        return final_topics

        # topics = {}
        # for item in texts:
        #     phrases = KeyPhrase.extract(item['text'])
        #     for phrase in phrases:
        #         if phrase not in topics:
        #             topics[phrase] = 0

        #         if phrase not in ignore:
        #             topics[phrase] = topics[phrase] + 1

        # recast = []
        # for topic in topics:
        #     recast.append({
        #         'topic': topic,
        #         'count': topics[topic]
        #     })

        # return sorted(Topics.dedupe(recast), key=lambda topic: topic['count'], reverse=True)[0:count]

    @staticmethod
    def similarity(primary, secondary):
        primary_split = primary.split(' ')
        secondary_split = secondary.split(' ')

        result = {
            'score': 0,
            'text': None
        }

        matches = []
        for word in secondary_split:
            if word in primary_split:
                matches.append(word)

        
        if len(matches) > 1:
            result['text'] = ' '.join(matches)
            result['score'] = (len(matches) * 2) / (len(primary_split) + len(secondary_split))
        
        return result

        



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


        
                