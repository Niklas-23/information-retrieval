import abc
from typing import Union, Tuple, List

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic


class PreProcessor(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'forward') and
                callable(subclass.forward) or
                NotImplemented)

    @abc.abstractmethod
    def forward(selfqueries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Union[Question, Answer]]:
        """Runs a PostProcessing against an incoming ranked document collection"""
        raise NotImplementedError