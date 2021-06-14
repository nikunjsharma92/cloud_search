from database import db, bcrypt
import datetime
import jwt
import os
from src.models.blacklist_tokens import BlacklistToken


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    auth_token = db.Column(db.String(1023), default=None)
    registered_on = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, int(os.getenv('BCRYPT_LOG_ROUNDS'))
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.created_on = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()

    @staticmethod
    def get_by_id(id):
        user = User.query.filter_by(id=id).first()
        return user

    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def update(self):
        self.updated_on = datetime.datetime.utcnow()
        return db.session.commit()

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=180),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'), algorithms='HS256')
        is_blacklisted_token = BlacklistToken.get_by_token(auth_token)
        if is_blacklisted_token:
            raise jwt.InvalidTokenError("Token is blacklisted")
        else:
            return int(payload['sub'])

