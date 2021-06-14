from flask_restful import Resource

from src.adapters.input_adapters.logout_input_adapter import LogoutInputAdapter
from src.usecases.user_management import UserManagement
from src.utils.authorize import authorize


class Logout(Resource):
    @authorize
    def post(self, user):
        parsed_args = LogoutInputAdapter().parse_post_request()
        UserManagement().logout(user, parsed_args[LogoutInputAdapter.AUTH_TOKEN])
        return {
            'status': 'succcess',
            'message': 'Successffully logged out.',
        }