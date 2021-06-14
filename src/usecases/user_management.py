from src.models.users import User


class UserManagement:
    def basic_login(self, email, password):
        user = User.query.filter(email=email, password=password).first()
        if not user:
            raise Exception("UserNotFound")

        user.access_token =

