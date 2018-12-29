import argparse
import json
import re
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('--text', help='Text to classify')
args = parser.parse_args()

nlp = spacy.load('en')

def preprocess(text):
  parsed = nlp(text)

  tagged_sent = [(w.text, w.tag_) for w in parsed]
  normalized_sent = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_sent]
  normalized_sent[0] = normalized_sent[0].capitalize()

  return re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))

def process(text):
  modified = preprocess(text)
  print(modified)
  parsed = nlp(modified)


process(args.text)