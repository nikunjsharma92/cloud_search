import jwt

from src.models.blacklist_tokens import BlacklistToken
from src.models.users import User
from database import bcrypt, db


class UserManagement:
    def register(self, email, password):
        existing_user = User.get_by_email(email)
        if existing_user:
            raise Exception("UserAlreadyExists")

        user = User(
            email=email,
            password=password,
        )
        user.save()
        return True

    def basic_login(self, email, password):
        user = User.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            raise Exception("UserNotFound")

        auth_token = user.encode_auth_token(user.id)
        return auth_token

    def logout(self, user, auth_token):
        try:
            User.decode_auth_token(auth_token)
        except jwt.InvalidTokenError:
            return True

        blacklist_token = BlacklistToken(token=auth_token)
        blacklist_token.save()
        return True
