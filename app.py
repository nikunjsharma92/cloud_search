from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv
from src.deliveries.http.sync import Sync

app = Flask(__name__)
api = Api(app)

load_dotenv()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Sync, '/sync')


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
