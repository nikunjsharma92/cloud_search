import os
from dotenv import load_dotenv
load_dotenv()

from elasticsearch_dsl.connections import connections
connections.create_connection(alias='es_conn', hosts=[os.getenv('ELASTIC_SEARCH_NODE')])
