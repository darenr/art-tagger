#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import sys
import codecs
import urllib3
import re
import json
import time
import sys

urllib3.disable_warnings()

index = 'art_dna'
doc_type = 'genes'


def pre_process_definition(text):
    # find tags
    tags = [x.lower() for x in re.findall('\[(.*?)\]', text)]
    # now remove all text between () and []
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    return (tags, text)

def load_data(es, filename="data/genes.json"):

    if es.indices.exists(index=index):
        print ' *', es.indices.delete(index=index)

    analyzer_settings = {
        "analyzer": {
            "analyzer_genes": {
                "tokenizer": "keyword",
                "filter": "lowercase"
            },
            "analyzer_general": {
              "tokenizer": "standard",
              "filter": "lowercase"
            }
        }
    }

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": analyzer_settings
        }
    }

    print ' *', es.indices.create(index=index, body=request_body)

    schema = {
        doc_type: {
            "properties": {
                "gene": {
                    "store": "true",
                    "type": "string",
                    "term_vector": "yes",
                    "analyzer": "analyzer_genes"
                },
                "tags": {
                    "store": "true",
                    "type": "string",
                    "term_vector": "yes",
                    "analyzer": "analyzer_genes"
                },
                "normalized_type":{
                    "store": "true",
                    "type": "string",
                    "term_vector": "yes",
                    "analyzer": "analyzer_genes"
                },
                "definition": {
                    "store": "true",
                    "type": "string",
                    "term_vector": "yes",
                    "analyzer": "analyzer_general"
                }
            }
        }
    }

    print ' *', es.indices.put_mapping(index=index, doc_type=doc_type, body=schema)
    print ' *', 'begin indexing...'

    for row in json.loads(open(filename).read()):
        id = row['ID']
        gene = row['name']
        normalized_type = row['normalized_type']
        if normalized_type in ["Broad Category", "Broad Medium", "Content: People and Figures/Portraits/Social Life"]:
          continue
        tags, definition = pre_process_definition(row['Definition'])
        try:
            r = es.index(index=index, doc_type=doc_type, id=id, body={
              "gene": gene,
              "tags": tags,
              "normalized_type": normalized_type,
              "definition": definition
            })
        except KeyboardInterrupt:
            raise
        except Exception, e:
            print artists, text
            print 'Failed', e
            sys.exit(0)

    # let the index catch up
    time.sleep(5)
    print ' *', es.count(index=index)['count'], 'gene categories rows loaded'


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print 'usage: <localhost|prod>'
        sys.exit(-1)
    else:
        if sys.argv[1] == 'localhost':
            print ' *', 'loading localhost elasticsearch'
            es = Elasticsearch(['http://localhost:9200'])
        else:
            print ' *', 'loading bonsai.io elasticsearch'
            es = Elasticsearch(
                ['https://x6c8diiv:z893nc4gjuq380lw@smoke-4703082.us-east-1.bonsai.io'])

        load_data(es=es)
