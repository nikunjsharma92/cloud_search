import abc

from src.lib.content_extractor.adapters.content_extractor_response_adapter import ContentExtractorResponse


class ContentExtractorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'extract_from_buffer') and
                callable(subclass.extract_from_buffer) and
                hasattr(subclass, 'extract_from_file') and
                callable(subclass.extract_from_file) or
                NotImplemented)

    @abc.abstractmethod
    def extract_from_buffer(self, buffer) -> ContentExtractorResponse:
        raise NotImplementedError()

    @abc.abstractmethod
    def extract_from_file(self, filepath: str) -> ContentExtractorResponse:
        raise NotImplementedError()
