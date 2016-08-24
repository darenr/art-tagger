#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import sys
import codecs
import urllib3
import re
import time
import sys
import json
from textblob import TextBlob

urllib3.disable_warnings()

index = 'art_dna'
doc_type = 'genes'

def more_like_this(es, artist_name, text):
    print ' *', artist_name
    blob = TextBlob(text)
    definition = ', '.join(blob.noun_phrases)
    print ' *', text
    search_body = {
        "size": 6,
        "query": {
            "bool": {
                "should": [
                    {"match": {"tags": artist_name}},
                    {"more_like_this": {
                        "fields": ["definition"],
                        "like": {
                            "doc": {
                                "definition": definition
                            }
                        },
                        "min_term_freq": 1,
                        "min_doc_freq": 1,
                        "minimum_should_match": "15%",
                      }
                    }
                ]
            }
        }
    }

    sr = es.search(index=index, body=search_body)
    if sr['hits']['total']:
        for hit in sr['hits']['hits']:
            print hit['_score'], 'Gene:', '***', hit['_source']['gene'], '***', '(type:', hit['_source']['normalized_type'],')'

def test(es):
    more_like_this(es, 'Catherine Opie', u"Catherine Opie candid photograph Cathy (bed Self-portrait) (1987) shows the artist atop a bed wearing a negligee and a dildo; the latter is attached to a whip that she holds in her teeth. Opie is known for her honest portraits of diverse individuals, from LGBT people to football players, and the self-portrait has also been a long-standing and important part of her practice. Instead of hiding her sexuality and interest in sadomasochism, Opie wears it proudly. Photographed at a time when artistic freedoms were generally under attack in America, Opie's full-frontal reveal is a kind of revolutionary moment, signifying that expression cannot and will not be suppressed.")
    more_like_this(es, 'John Baldessari', u"The voids in Baldessari's painted photographs are simultaneously positive and negative spaces, both additive and subtractive. Person In Person with Pillow: Desire, Lust, Fate, a woman's facial expression is obscured by such void, leaving only her posture to suggest her emotional state. The two images stacked above the woman can be read as comic-style thought bubbles, intimating that she has lust, desire, and fate on her mind.")
    more_like_this(es, 'Nan Goldin', u"Self-Portrait in blue bathroom, London ‐ \"Self-portrait in blue bathroom, London\" is part of The Ballad of Sexual Dependency, Nan Goldin’s well known photographic series, that originally toured clubs, museums, and galleries as a slide show set to music. Captured over ten years beginning in 1976, this body of work focused on the drug culture, sexual relations, and intimate moments in the everyday lives of the group Goldin called her tribe, in New York’s East Village. The photographs from “The Ballad of Sexual Dependency” published as a book of the same title in 1986, constituted a record of countercultural life before the overwhelming reality of the AIDS crisis entered the public consciousness. For Goldin, who in her later work confronted the impact of AIDS on the lives of her close friends, this series was a testament of both love and loss.  Goldin’s scenes in “The Ballad of Sexual Dependency” are often convivial but are overwhelmed by self-indulgence and debauchery: a figure preparing to use drugs, two men embracing on the beach amid cans of Budweiser, or a couple having sex in an unkempt apartment. Candidly portraying outsiders, she emerged from the lineage of Lisette Model, who capture almost ethnographic studies of the disenfranchised, and Diane Arbus, who addressed her subjects with empathy, though often emphasizing their marginalized status. Goldin, a documentary photographer, had a real-life intimacy with her subjects, many of whom would have been considered depraved by the mainstream public.  The self-portrait in The Jewish Museum’s collection was the first in a series of photographs from “The Ballad of Sexual Dependency” depicting Goldin’s friends studying themselves in the mirror. The soundtrack for this segment of the slide show was a 1967 song by the alternative rock band Velvet Underground. It began: “I’ll be your mirror/Reflect what you are, in case you don’t know/I’ll be the wind, the rain and the sunset/The light on your door to show that you’re home.” In Goldin’s other mirror images, she focuses on her subjects being consumed with their likenesses. In this case, however, Goldin identifies with the camera itself, and her ethereal reflection stares back at it, and therefore at the viewer, rather than at her own face. Unlike some of her more explicit depictions of her subjects performing ablutions, Goldin’s image hovering in the background resembles an early Christian icon: a metallic frame surrounds her face, and her illuminated skin glows against the azure wall.  In many of Goldin’s works, she follows her friends into their showers and bathtubs. For her, purity and tenderness lie not in the cleansing that occurs in the bathroom but in her subjects’ ability to make themselves vulnerable to her and her camera. In this self-portrait, the bathroom itself assumes center stage. The sanitizing objects-bottles of Dettol antiseptic, bathroom cleanser, and a loofah sponge propped at the side of the bathtub-exacerbate the harsh atmosphere created by the coarse walls that overwhelm the picture. The bathroom becomes a site of self-examination and physical manipulation, and it is within these intimate surroundings that Goldin reveals herself.")
    more_like_this(es, 'Todd Hido', u"The two pieces in the Kadist Collection depict foggy landscapes, one at dawn, the other at nighttime. Both dimly lit scenes are dominated by an eerie feeling. Taken by a road, these painterly photographs suggest the uncanny character of the transient. Deeply interested in the topic of housing in the United States, Todd Hido's large, colored photographs of American suburbia emphasize feelings of isolation and anonymity. Heavily influenced by Larry Sultan's work, Hido's images have a very narrative, almost cinematic quality to them. Northern Californian fog frequently recurs in his photographs has become one of his most recognizable trademarks.")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print 'usage: <localhost|prod>'
        sys.exit(-1)
    else:
        if sys.argv[1] == 'localhost':
            print ' *', 'using localhost elasticsearch'
            es = Elasticsearch(['http://localhost:9200'])
        else:
            print ' *', 'using bonsai.io elasticsearch'
            es = Elasticsearch(
                ['https://x6c8diiv:z893nc4gjuq380lw@smoke-4703082.us-east-1.bonsai.io'])

        test(es=es)
