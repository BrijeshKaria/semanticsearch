from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
from bert_serving.client import BertClient
bc = BertClient()
es = Elasticsearch([{'host':'localhost','port':9200}])
def getQuotes():
    f = open('./quotes.txt', 'r')
    for line in f:
        quote = line.strip().lower()
        if (len(quote.split()) <= 510): # 510 IS THE MAX
            vector = bc.encode([quote])[0].tolist()
            yield {
                "_index": 'bertdemo',
                "quote" : quote,
                "vector" : vector
             }
bulk(client=es, actions = getQuotes(), chunk_size=1000, request_timeout = 120)
print("Quotes uploaded.")