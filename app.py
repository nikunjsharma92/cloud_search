from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_migrate import Migrate
from src.models import *
from src.deliveries.http.authenticate_provider import AuthenticateProvider
from src.deliveries.http.authorize_provider import AuthorizeProvider
from src.deliveries.http.login import Login
from src.deliveries.http.logout import Logout
from src.deliveries.http.register import Register
from src.deliveries.http.sync_files import Sync
load_dotenv()

import os
from database import db, bcrypt
# from routes import initialize_routes


def create_app(name):
    app = Flask(name)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MASTER_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    api = Api(app)
    api.add_resource(AuthorizeProvider, '/<provider>/authorize')
    api.add_resource(AuthenticateProvider, '/<provider>/authenticate')
    api.add_resource(Sync, '/<provider>/sync')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')

    return app


app = create_app(__name__)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
