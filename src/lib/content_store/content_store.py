
class ContentStore:
    def __init__(self, client):
        self.__client = client

    def add_doc(self, id, metadata, content):
        return self.__client.add_doc(id, metadata, content)

    def update_doc(self, id, new_content):
        return self.__client.update_doc(id, new_content)