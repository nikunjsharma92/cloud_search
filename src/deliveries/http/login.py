from flask_restful import Resource

from src.adapters.input_adapters.login_input_adapter import LoginInputAdapter
from src.usecases.user_management import UserManagement


class Login(Resource):
    def post(self):
        parsed_args = LoginInputAdapter().parse_post_request()
        auth_token = UserManagement().basic_login(parsed_args[LoginInputAdapter.EMAIL], parsed_args[LoginInputAdapter.PASSWORD])
        return {
            'status': 'succcess',
            'message': 'Logged in successfully',
            'auth_token': auth_token
        }