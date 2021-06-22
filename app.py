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

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MASTER_DB_URI')
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
