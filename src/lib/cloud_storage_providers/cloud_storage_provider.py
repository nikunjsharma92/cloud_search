class CloudStorageProvider:
    def __init__(self, client):
        self.__client = client

    def authorize(self, **args):
        return self.__client.authorize(**args)

    def authenticate(self, code):
        return self.__client.authenticate(code)

    def init_client(self, access_token):
        return self.__client.init_client(access_token)

    def sync(self, *args):
        return self.__client.sync(*args)
