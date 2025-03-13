from typing import List, Union, Tuple

from flaskapp.classification.abstract_models import AbstractFindWordsModel
from flaskapp.classification.data_structure import SearchTerm
from flaskapp.classification.finder_gram_levenshtein_model import FinderGramLevenshteinModel


# TODO implement the logic on document classifier
class DocumentClassifier:

    def __init__(self, ocr_data_collection: List[Tuple[str, dict]],
                 find_words_model: AbstractFindWordsModel = FinderGramLevenshteinModel):
        """
        Try to classify a set of ocr data structure.

        :param ocr_data_collection: Expect to be a list of Tuple(id, data). The Tuple must contain and id for
            each page and its ocr_data. Where ocr_data must be an dict with the following structure:
            {words: [ {box: {x0: float, xf: float, y0: float, yf: float}, confidence: float, text: str} ], text: str}
        :param find_words_model: The find words model to be used
        """

        self.__find_words_model = find_words_model
        self.__ocr_data_collection = ocr_data_collection

    def classify_document(self, search_terms: List[str], no_relevant_terms: Union[List[str], None] = None,
                          max_percentage_error=0.2):
        pass

    def get_classification_per_page(self) -> Tuple[str, SearchTerm]:
        pass
