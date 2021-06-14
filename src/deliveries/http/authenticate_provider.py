from flask_restful import Resource
from src.adapters.input_adapters.authenticate_input_adapter import AuthenticateInputAdapter
from src.usecases.cloud_storage_provider_management import CloudStorageProviderManagement
from src.utils.authorize import authorize


class AuthenticateProvider(Resource):
    @authorize
    def post(self, user, provider):
        parsed_request = AuthenticateInputAdapter().parse_post_request()

        authentication_response = CloudStorageProviderManagement().authenticate(user, provider, parsed_request[AuthenticateInputAdapter.CODE])

        return {
            'status': 'success',
            'access_token': authentication_response.access_token,
            'message': 'Successfully authenticated provider'
        }, 200
