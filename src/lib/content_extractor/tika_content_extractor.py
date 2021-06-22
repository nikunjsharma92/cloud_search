import tika
from tika import parser
import os

from src.lib.content_extractor.adapters.content_extractor_response_adapter import ContentExtractorResponse
from src.lib.content_extractor.content_extractor_interface import ContentExtractorInterface


class TikaContentExtractor(ContentExtractorInterface):
    def __init__(self):
        self.__client = tika
        self.__client.TikaClientOnly = True
        self.__client.TikaServerEndpoint = os.getenv('TIKA_ENDPOINT')

    def extract_from_buffer(self, buffer) -> ContentExtractorResponse:
        response = self.__client.parser.from_buffer(buffer)
        return ContentExtractorResponse(content=response['content'])

    def extract_from_file(self, filepath: str) -> ContentExtractorResponse:
        response = self.__client.parser.from_file(filepath)
        return ContentExtractorResponse(content=response['content'])
