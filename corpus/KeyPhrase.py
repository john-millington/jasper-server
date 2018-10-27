import nltk
import re

from nltk.corpus import stopwords

GRAMMAR = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

class KeyPhrase:
    TWITTER_REGEX = re.compile(r"(@[^\s]+\s+)|(#(?=[^\s]+))")
    URLS_REGEX = re.compile(r"(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?\s?")
    REGEX = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'

    LEMMATIZER = nltk.WordNetLemmatizer()
    STEMMER = nltk.stem.porter.PorterStemmer()
    CHUNKER = nltk.RegexpParser(GRAMMAR)
    STOPWORDS = stopwords.words('english')

    @staticmethod
    def extract(string):
        modified = string

        try:
            modified = re.sub(KeyPhrase.TWITTER_REGEX, '', modified)
            modified = re.sub(KeyPhrase.URLS_REGEX, '', modified)
        except:
            pass

        return KeyPhrase.get_terms(KeyPhrase.tree(modified))


    @staticmethod
    def tree(string):
        toks = nltk.regexp_tokenize(string, KeyPhrase.REGEX)
        postoks = nltk.tag.pos_tag(toks)
        
        return KeyPhrase.CHUNKER.parse(postoks)


    @staticmethod
    def leaves(tree):
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()


    @staticmethod
    def normalise(word):
        word = word.lower()
        # word = stemmer.stem_word(word) #if we consider stemmer then results comes with stemmed word, but in this case word will not match with comment
        word = KeyPhrase.LEMMATIZER.lemmatize(word)

        return word


    @staticmethod
    def acceptable_word(word):
        accepted = bool(2 <= len(word) <= 40
            and word.lower() not in KeyPhrase.STOPWORDS)

        return accepted


    @staticmethod
    def get_terms(tree):
        terms = []
        for leaf in KeyPhrase.leaves(tree):
            phrase = [ KeyPhrase.normalise(w) for w,t in leaf if KeyPhrase.acceptable_word(w) ]
            if len(phrase) > 1 and len(phrase) < 5:
                terms.append(' '.join(phrase))

        return terms