from elasticsearch_dsl import Document, Date, Integer, Text, UpdateByQuery, Q
import elasticsearch_connection


class FileContent(Document):
    file_id = Integer()
    user_id = Integer()
    content = Text() # TODO: analyzer
    created_on = Date()
    updated_on = Date()

    class Index:
        name = 'files_content_store'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(FileContent, self).save(**kwargs, using='es_conn')

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
        q = Q("match", user_id=user_id) & Q("match", content=querystring)
        return super(FileContent, self).search(using='es_conn').query(q)
