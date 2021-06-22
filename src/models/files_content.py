from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, UpdateByQuery, Search


class FileContent(Document):
    file_id = Integer()
    user_id = Integer()
    content = Text() #Text(analyzer='snowball')
    created_on = Date()
    updated_on = Date()

    class Index:
        name = 'files_content-temp3'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(FileContent, self).save(**kwargs)

    def append_content(self, new_content):
        ubq = UpdateByQuery(index=self.Index.name)
        ubq.update_from_dict({
            "script": {
                "inline": "ctx._source.content += '{}'".format(new_content),
                "lang": "painless"
            },
            "query": {
                "match": {
                    "_id": self.meta.id
                }
            }
        })
        resp = ubq.execute()

    def search_content(self, user_id: int, querystring: str):
        return super(FileContent, self).search().query("match", content=querystring, user_id=user_id)
