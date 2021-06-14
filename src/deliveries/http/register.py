from flask_restful import Resource
from src.adapters.input_adapters.register_input_adapter import RegisterInputAdapter
from src.usecases.user_management import UserManagement


class Register(Resource):
    def post(self):
        parsed_args = RegisterInputAdapter().parse_post_request()
        UserManagement().register(parsed_args[RegisterInputAdapter.EMAIL],
                                                  parsed_args[RegisterInputAdapter.PASSWORD])
        return {
            'status': 'succcess',
            'message': 'Registered Successfully. Please signin to your account',
        }

