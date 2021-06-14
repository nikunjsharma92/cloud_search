from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
from src.models import *

load_dotenv()

import os
from database import db, bcrypt
from routes import initialize_routes


def create_app(name):
    app = Flask(name)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MASTER_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    api = Api(app)
    initialize_routes(api)

    return app


app = create_app(__name__)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
