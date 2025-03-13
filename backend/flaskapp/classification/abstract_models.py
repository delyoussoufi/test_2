from abc import ABCMeta, abstractmethod
from typing import List, Union

from flaskapp.classification.data_structure import SearchTerm


class AbstractFindWordsModel(metaclass=ABCMeta):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def find_words(cls, ocr_data: dict, search_terms: List[str],
                   no_relevant_terms: Union[List[str], None] = None,
                   black_list_terms: Union[List[str], None] = None,
                   max_percentage_error=0.2) -> List[SearchTerm]:
        """

        :param ocr_data: It must but a dict as such:
            {words: [ {box: {x0: float, xf: float, y0: float, yf: float}, confidence: float, text: str} ], text: str}
        :param search_terms:
        :param no_relevant_terms:
        :param black_list_terms:
        :param max_percentage_error:
        :return:
        """
        pass
