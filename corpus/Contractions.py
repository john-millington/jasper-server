import json
import re

cList = json.load(open('./corpus/data/contractions.json'))

class Contractions:
    REGEX = re.compile('(%s)' % '|'.join(cList.keys()))

    @staticmethod
    def expand(string):
        def replace(match):
            return cList[match.group(0)]

        return Contractions.REGEX.sub(replace, string)