from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv

from src.deliveries.http.authenticate import Authenticate
from src.deliveries.http.authorize import Authorize
from src.deliveries.http.sync import Sync

app = Flask(__name__)
api = Api(app)

load_dotenv()

api.add_resource(Authorize, '/<provider>/authorize')
api.add_resource(Authenticate, '/<provider>/authenticate')
api.add_resource(Sync, '/sync')



if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
