from bert_serving.client import BertClient
bc = BertClient()

from elasticsearch import Elasticsearch
client = Elasticsearch([{'host':'localhost','port':9200}])

def findRelevantHits (inQuiry):
    inQuiry_vector = bc.encode([inQuiry])[0].tolist()
    queries = {
        'bert': {
           "script_score": {
              "query": {
                 "match_all": {}
               },
               "script": {
                  "source": "cosineSimilarity(params.inQuiry_vector, doc['vector']) + 1.0",
                  "params": {
                     "inQuiry_vector": inQuiry_vector
                   }
                }
           }
        },
        'mlt': {
                "more_like_this": {
                        "fields": ["quote"],
                        "like": inQuiry,
                        "min_term_freq": 1,
                        "max_query_terms": 50,
                        "min_doc_freq": 1
                }
        }
    }

    result = {'bert' : [], 'mlt' : [] }

    for metric, query in queries.items():
        body = { "query": query, "size" : 10, "_source" : ["quote"] }
        response = client.search(index='bertdemo',body=body, request_timeout=120)
        #print(response)
        result[metric] = [a['_source']['quote'] for a in response['hits']['hits']]
    return result

inQuiry = "Most folks are about as happy as they make up their minds to be"
result = findRelevantHits (inQuiry.strip().lower())
print(result)