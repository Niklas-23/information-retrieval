import abc
from typing import Union, Tuple, List

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic


class PostProcessor(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'forward') and
                callable(subclass.forward) or
                NotImplemented)

    @abc.abstractmethod
    def forward(self, queries: List[Topic], documents: List[Tuple[Topic, Union[Question, Answer], float]]) -> List[Tuple[Topic, Union[Question, Answer], float]]:
        """Runs a PostProcessing against an incoming ranked document collection"""
        raise NotImplementedError