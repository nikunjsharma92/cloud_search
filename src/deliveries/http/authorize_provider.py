from flask_restful import Resource
from dropbox import DropboxOAuth2FlowNoRedirect


class Authorize(Resource):
    # get and save tokens from services like drropbox and google drive
    def get(self, provider):
        # return {
        #     'authorization_url': 'https://www.dropbox.com/oauth2/authorize?client_id={}&response_type=code'.format('5q28gt6qyndwadq')
        # }
        return DropboxOAuth2FlowNoRedirect(consumer_key='5q28gt6qyndwadq', consumer_secret='nt7vu3ycirob5db', token_access_type='online', locale='en').start()
        # cloud_storage_provider = CloudStorageProvider(provider)
        # return {'authorization_url': 'cloud_storage_provider.get_authorization_url()'}


    def post(self):
        pass

    def put(self):
        pass
