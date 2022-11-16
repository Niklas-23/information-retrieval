import abc
from typing import List
from arqmath_code.topic_file_reader import Topic


class QueryPreProcessor(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'forward') and
                callable(subclass.forward) or
                NotImplemented)

    def __call__(self, queries: List[Topic]) -> List[Topic]:
        return self.forward(queries=queries)

    @abc.abstractmethod
    def forward(self, queries: List[Topic]) -> List[Topic]:
        """Runs a PostProcessing against an incoming ranked document collection"""
        raise NotImplementedError
