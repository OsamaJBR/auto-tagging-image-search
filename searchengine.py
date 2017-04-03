from datetime import datetime
from elasticsearch import Elasticsearch

class SEngine():
    def __init__(self,config):
        self.elasticsearch_hosts=config.get('elasticsearch','hosts')
        self.elasticsearch_index=config.get('elasticsearch','index')
        self.translated_language=config.get('translation','target')

    def push_to_es(self,doc):
        es = Elasticsearch(hosts=self.elasticsearch_hosts)
        res = es.index(
                index=self.elasticsearch_index,
                body=doc,
                doc_type='image',
                refresh=True,
                )
        return res['created']
    
    def search_for_words(self,op,words):
        es = Elasticsearch(hosts=self.elasticsearch_hosts)
        query = {
            "size": 20,
            "sort": {
                "_score": "desc"
            },
            "query":{
                "multi_match" : {
                    "query": words,
                    "fields": [ "image_fname", "en_lables", "%s_lables" %self.translated_language ],
                    "operator" : op
                }
            }
        }
        res = es.search(index=self.elasticsearch_index, body=query)
        images = []
        if res['hits']['total'] :
            for hit in res['hits']['hits']:
                images.append({"filename" : hit['image_fname'],"path" : hit['image_path']})
        return images