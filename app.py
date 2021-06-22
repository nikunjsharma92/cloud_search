from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

from routes import initialize_routes
from database import db, bcrypt
import elasticsearch_connection
from src.models import *


def create_app(name):
    app = Flask(name)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+\
                                            os.getenv('MASTERDB_USER') + ':' + os.getenv('MASTERDB_PASSWORD') + \
                                            '@' + os.getenv('MASTERDB_HOST') + ':'+os.getenv('MASTERDB_PORT') + \
                                            '/' + os.getenv('MASTERDB_DB')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    api = Api(app)
    initialize_routes(api)
    return app

load_dotenv()

app = create_app(__name__)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
