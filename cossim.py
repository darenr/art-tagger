#!/usr/bin/env python
# -*- coding: utf-8 -*--

import unicodecsv as csv
import sys
import codecs
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
  return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
  return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

opie = '''
Catherine Opie candid photograph Cathy (bed Self-portrait) (1987) shows the artist atop a bed wearing a negligee and a dildo; the latter is attached to a whip that she holds in her teeth. Opie is known for her honest portraits of diverse individuals, from LGBT people to football players, and the self-portrait has also been a long-standing and important part of her practice. Instead of hiding her sexuality and interest in sadomasochism, Opie wears it proudly. Photographed at a time when artistic freedoms were generally under attack in America, Opie's full-frontal reveal is a kind of revolutionary moment, signifying that expression cannot and will not be suppressed. 
Since the 1990s, Catherine Opie has been recognized for her use of documentary photography to address issues of community and queerness, and the ways in which identity is shaped by architecture. Particularly resonant during the Culture Wars of the 1980s and early 1990s a time in which the religious right tried to impose itself as a political force and cultural censor Opie's photographs privilege the representation of specific communities, whether the LGBT, teenagers, surfers, football players, or her group of friends who engage in sexual role playing, tattooing, and piercing.
'''

print normalize(opie)

print 'test', cosine_sim('Artists who attended the California Institute of the Arts, in Valencia, California. Since its founding in 1961, CalArts has become one of the most influential art schools in the United States. Since the early 1970s, CalArts’ School of Art has educated more than 15,000 alumni around the globe and has produced an exceptional number of internationally renowned artists, including [John Baldessari](/artist/john-baldessari), [Ross Bleckner](/artist/ross-bleckner), [Mark Bradford](/artist/mark-bradford), [Eric Fischl](/artist/eric-fischl), [Elad Lassry](/artist/elad-lassry), [Catherine Opie](/artist/catherine-opie), and [David Salle](/artist/david-salle).', opie)

sys.exit(-1)

d = defaultdict(float)

with open('genes.csv', 'r') as f:
  for row in csv.reader(f):
    d[row[2]] = cosine_sim(opie, row[4])

for w in sorted(d, key=d.get, reverse=True)[:50]:
  print w, d[w]




