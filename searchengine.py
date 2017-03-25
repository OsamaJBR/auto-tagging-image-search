from datetime import datetime
from elasticsearch import Elasticsearch

class SEngine():
    def __init__(self,config):
        self.elasticsearch_hosts=config.get('elasticsearch','hosts')
        self.elasticsearch_index=config.get('elasticsearch','index')

    def push_to_es(self,doc):
        es = Elasticsearch(hosts=self.elasticsearch_hosts)
        res = es.index(
                index=self.elasticsearch_index,
                body=doc,
                doc_type='image',
                refresh=True,
                )
        return res['created']
    