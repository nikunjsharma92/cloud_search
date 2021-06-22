import os
from dotenv import load_dotenv
load_dotenv()

from elasticsearch_dsl.connections import connections
print("ELASTIC ENV: ", os.getenv('ELASTIC_SEARCH_URI'))
connections.create_connection(hosts=[os.getenv('ELASTIC_SEARCH_URI')])
