import abc


class CloudStorageProviderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'authorize') and
                callable(subclass.authorize) and
                hasattr(subclass, 'authenticate') and
                callable(subclass.authenticate) and
                hasattr(subclass, 'init_client') and
                callable(subclass.init_client) and
                hasattr(subclass, 'get_file_list') and
                callable(subclass.get_file_list) and
                hasattr(subclass, 'get_file_content') and
                callable(subclass.get_file_content) and
                hasattr(subclass, 'download_file_content') and
                callable(subclass.download_file_content) or
                NotImplemented)

    @abc.abstractmethod
    def authorize(self, **args):
        raise NotImplementedError()

    @abc.abstractmethod
    def authenticate(self, code: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def init_client(self, access_token: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_file_list(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_file_content(self, path: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def download_file_content(self, file_path: str):
        raise NotImplementedError()
