from datetime import datetime
from elasticsearch import Elasticsearch


class ElasticContentStore:
    def __init__(self, uri):
        self.__client = Elasticsearch([uri])
        self.__index = 'content-store'

    # def add_doc(self, id, metadata, content):
    #     doc = {
    #         'metadata': metadata,
    #         'text': content,
    #         'timestamp': datetime.now(),
    #     }
    #     return self.__client.index(index=self.__index, id=id, body=doc)
    #
    # es.indices.refresh(index="test-index")
    #
    # def append_content(self, id, new_content):
    #     return self.__client.update(
    #         index=self.__index,
    #         id=id,
    #         body={"script": "ctx._source.content+="+new_content}
    #     )
    #
    # es.indices.refresh(index="test-index")
    #
    # def delete_content(self, id):
    #     return self.__client.update(index=self.__index,
    #         id=id, body={"script": "ctx._source.content=''"})
    #
    # es.indices.refresh(index="test-index")
    #
