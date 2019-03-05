import argparse
import json
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('--text', help='Text to classify')
args = parser.parse_args()

nlp = spacy.load('en')
parsed = nlp(args.text)

def get_perspective(tree, subjects = [], allow_modifiers = False, allow_preps = False):
  for item in tree:
    if allow_preps == False and item['arc'] == 'prep':
      continue

    elif item['arc'] == 'nsubj' or item['arc'] == 'dobj' or item['arc'] == 'pobj':
      if item['NE'] != '' and item['NE'] != 'DATE':
        subjects.append(item['word'])

        if len(item['modifiers']) > 0:
          subjects = get_perspective(item['modifiers'], subjects, True, allow_preps)

      elif len(item['modifiers']) > 0:
        subjects = get_perspective(item['modifiers'], subjects, True, allow_preps)


    elif allow_modifiers == True and item['arc'] == 'conj' or item['arc'] == 'appos':
      if item['NE'] != '' and item['NE'] != 'DATE':
        subjects.append(item['word'])

        if len(item['modifiers']) > 0:
            subjects = get_perspective(item['modifiers'], subjects, True, allow_preps)
        
      elif len(item['modifiers']) > 0:
        subjects = get_perspective(item['modifiers'], subjects, True, allow_preps)


    elif len(item['modifiers']) > 0:
      subjects = get_perspective(item['modifiers'], subjects, False, allow_preps)

  
  if len(subjects) == 0 and allow_preps == False:
    subjects = get_perspective(tree, subjects, False, True)


  return subjects

print(json.dumps({
  'subjects': get_perspective(parsed.print_tree()),
  # 'tree': parsed.print_tree()
}, indent=4, sort_keys=True))