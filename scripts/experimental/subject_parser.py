import argparse
import json
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('--text', help='Text to classify')
args = parser.parse_args()

nlp = spacy.load('en')
parsed = nlp(args.text)

subjects = []
direct = []
indirect = []
attributional = []

def noun_phrase(item):
    ignore = [
        'det',
        'prep',
        'relcl',
        'punct'
    ]

    complete = []
    for text in item.lefts:
        if text.dep_ not in ignore:
            complete.append(text.orth_)

    complete.append(item.orth_)

    for text in item.rights:
        if text.dep_ not in ignore:
            complete.append(text.orth_)

    return ' '.join(complete)

    # modified = items.copy()
    # modified.reverse()
    # modified.remove(item)

    # for text in modified:
    #     if text.dep_ in preceders:
    #         complete.append(text.orth_)
    #     else:
    #         break

    # complete.reverse()
    # return ' '.join(complete)

def get_primary_subject(tree, level = 1, subjects = []):
    ignore = [
        'which',
        'that',
        'it',
        'they',
        'he',
        'one'
    ]

    for item in tree:
        if len(item['modifiers']) > 0:
            subject = get_primary_subject(item['modifiers'], level + 1, subjects)

        if item['arc'] == 'nsubj':
            if item['word'].lower() not in ignore:
                subjects.append([item['word'], level])

    if (len(subjects)):
        reordered = sorted(subjects, key=lambda subject: subject[1], reverse=True)
        return reordered[0][0]

    return None
        

for text in parsed:
    if text.dep_ == 'nsubj' or text.dep_ == 'nsubjpass':
        subjects.append(noun_phrase(text))

    if text.dep_ == 'dobj':
        direct.append(noun_phrase(text))

    if text.dep_ == 'pobj':
        indirect.append(noun_phrase(text))

    if text.dep_ == 'attr':
        attributional.append(noun_phrase(text))

print(json.dumps({
    'subject': get_primary_subject(parsed.print_tree()),
    'subjects': subjects,
    'direct': direct,
    'indirect': indirect,
    'attributional': attributional
}, indent=4, sort_keys=True))