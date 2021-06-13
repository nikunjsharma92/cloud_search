from flask_restful import Resource
from dropbox import DropboxOAuth2FlowNoRedirect

from src.adapters.input_adapters.authenticate_input_adapter import AuthenticateInputAdapter


class Authenticate(Resource):
    # get and save tokens from services like dropbox and google drive
    def get(self, provider):
        return {'hello': 'world'}

    def post(self, provider):
        parsed_request = AuthenticateInputAdapter().parse_post_request()
        return DropboxOAuth2FlowNoRedirect(consumer_key='5q28gt6qyndwadq', consumer_secret='nt7vu3ycirob5db', token_access_type='online', locale='en').finish(parsed_request[AuthenticateInputAdapter.CODE]).access_token
        # cloud_storage_provider = CloudStorageProvider(provider)
        # return {'authorization_url': 'cloud_storage_provider.get_authorization_url()'}

    def put(self):
        pass
