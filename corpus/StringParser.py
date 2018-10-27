import re
import nltk
import string

from pattern.en import spelling
from nltk.corpus import wordnet
from symspell.SymSpell import SymSpell

from corpus.Contractions import Contractions

class StringParser:
    # Removes twitter mentions and the preceeding hash from hash tags
    TWITTER_REGEX = re.compile(r"(@[^\s]+\s+)|(#(?=[^\s]+))")
    URLS_REGEX = re.compile(r"(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?\s?")
    PUNCTUATION_TABLE = dict((ord(char), None) for char in string.punctuation)
    PUNCTUATION_REGEX = re.compile(r"[\?\!\—\(\)\[\]\{\}\,\.\-\|\"]?")
    LEMMATISER = nltk.WordNetLemmatizer()
    SPELLING = SymSpell()

    @staticmethod
    def correct(text):
        reduced = StringParser.reduce(text)
        corrected = StringParser.SPELLING.lookup(reduced, 0, 1)

        return corrected[0].term


    @staticmethod
    def parse(text):
        modified = Contractions.expand(text.lower())
        # modified = StringParser.correct(modified)

        try:
            modified = re.sub(StringParser.TWITTER_REGEX, '', modified)
            modified = re.sub(StringParser.URLS_REGEX, '', modified)
            modified = re.sub(StringParser.PUNCTUATION_REGEX, '', modified)
        except:
            pass

        # modified = modified.translate(StringParser.PUNCTUATION_TABLE)
        tokenised = nltk.word_tokenize(modified)
        pos_tags = nltk.pos_tag(tokenised)

        lemmatised = []
        for pos in pos_tags:
            wordnet_tag = StringParser.wordnet(pos[1])
            if (wordnet_tag != None):
                lemmatised.append(StringParser.LEMMATISER.lemmatize(pos[0], wordnet_tag))
            else:
                lemmatised.append(StringParser.LEMMATISER.lemmatize(pos[0]))

        return lemmatised
        

    @staticmethod
    def reduce(text):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", text)


    @staticmethod
    def wordnet(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None