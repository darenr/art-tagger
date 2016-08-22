#!/usr/bin/env python
# -*- coding: utf-8 -*--

import csv
import sys
import codecs
import re
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

#stemmer = nltk.stem.porter.PorterStemmer()
#stemmer = SnowballStemmer("english")

class NoStemmer():
  def stem(self, t):
    return t

stemmer = NoStemmer()

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def normalize(text):
    # force lowercase
    text = text.lower()
    # first tokenize by sentence, then by word to ensure that punctuation is
    # caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(
        text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw
    # punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]

opie = ('Catherine Opie', '''
Catherine Opie candid photograph Cathy (bed Self-portrait) (1987) shows the artist atop a bed wearing a negligee and a dildo; the latter is attached to a whip that she holds in her teeth. Opie is known for her honest portraits of diverse individuals, from LGBT people to football players, and the self-portrait has also been a long-standing and important part of her practice. Instead of hiding her sexuality and interest in sadomasochism, Opie wears it proudly. Photographed at a time when artistic freedoms were generally under attack in America, Opie's full-frontal reveal is a kind of revolutionary moment, signifying that expression cannot and will not be suppressed.

''')


def test():
    print 'test', cosine_sim('Artists who attended the California Institute of the Arts, in Valencia, California. Since its founding in 1961, CalArts has become one of the most influential art schools in the United States. Since the early 1970s, CalArts’ School of Art has educated more than 15,000 alumni around the globe and has produced an exceptional number of internationally renowned artists, including [John Baldessari](/artist/john-baldessari), [Ross Bleckner](/artist/ross-bleckner), [Mark Bradford](/artist/mark-bradford), [Eric Fischl](/artist/eric-fischl), [Elad Lassry](/artist/elad-lassry), [Catherine Opie](/artist/catherine-opie), and [David Salle](/artist/david-salle).', opie)
    sys.exit(-1)


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def pre_process_definition(text):
    # find artist names between [name]
    artists = [x.lower() for x in re.findall('\[(.*?)\]', text)]
    # now remove all text between () and []
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    return (artists, text)


def find_tags():
    d = defaultdict(float)

    for row in unicode_csv_reader(open('genes.csv')):
        artists, text = pre_process_definition(row[4])
        if opie[0].lower() in artists:
            d[(row[2], 'matched artist')] = 1.0
        else:
            d[(row[2], text)] = cosine_sim(opie[1], text)

    for w in sorted(d, key=d.get, reverse=True)[:5]:
        print w[0], d[w]


if __name__ == "__main__":
    # test()
    find_tags()
