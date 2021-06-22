from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from time import sleep
import requests

load_dotenv()

print("Checking for mysql readiness", flush=True)
while True:
    try:
        engine = create_engine(
              'mysql+pymysql://'+\
                os.getenv('MASTERDB_USER') + ':' + os.getenv('MASTERDB_PASSWORD') + \
                '@' + os.getenv('MASTERDB_HOST') + ':'+os.getenv('MASTERDB_PORT') + \
                '/' + os.getenv('MASTERDB_DB'))

        conn = engine.connect()
        r = conn.execute("SELECT 1 as value")
        break
    except Exception as e:
        print("MasterDb not ready. Retrying in 5 seconds....", flush=True)

    sleep(10)

print("MasterDb is ready")

while True:
    try:
        r = requests.get('http://'+os.getenv('ELASTIC_SEARCH_NODE'))
        if r.status_code == 200:
            break
        else:
            raise Exception("Elastic not ready")
    except Exception as e:
        print("Elastic not ready. Retrying in 5 seconds....", flush=True)

    sleep(5)


print("Elastic Ready")