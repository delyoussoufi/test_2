from typing import List, Union

import numpy as np

from ..abstract_models import AbstractFindWordsModel
from ..data_structure import FoundTerm, Box, SearchTerm
from .finder_gram_levenshtein import FinderGramLevenshtein


class FinderGramLevenshteinModel(AbstractFindWordsModel):
    """
       Model to find words in a orc_data using n-grams and Levenshtein edit distance strategy.

       Methods
       -------

       candidate_words_boxes(orc_data: dict)
           return list of candidate words and their respective boxes

       find_words(ocr_data, search_terms, no_relevant_terms=None, max_percentage_error=0.2,
            return a List of SearchTerm objects

       """

    def __init__(self):
        super(FinderGramLevenshteinModel, self).__init__()

    @classmethod
    def candidate_words_boxes(cls, orc_data: dict):
        """
        Return the list of candidate words and their boxes from a orc_data dictionary.

        :param orc_data: dictionary with a key words that contains the words from OCR data
        TODO: implement the data structure for the ORC data. It should receive dict or a data structure. The dictionary
        TODO: should be mapped to the data structure to validate the data.
        :return: return the list of words and boxes collected from the orc_data
        """
        words_dicts = orc_data.get("words", None)
        if words_dicts is None:
            raise AttributeError
        word_list = []
        box_list = []
        for word_dict_i in words_dicts:
            word_list.append(word_dict_i['text'])
            box_list.append(word_dict_i['box'])
        return np.array(word_list), np.array(box_list)

    @classmethod
    def find_words(
            cls,
            ocr_data: dict,
            search_terms: List[str],
            no_relevant_terms: Union[List[str], None] = None,
            black_list_terms: Union[List[str], None] = None,
            max_percentage_error=0.2
    ) -> List[SearchTerm]:
        """
        Find words in a fuzzy way, this strategy is a combination of n-grams search and levenshtein edit distance.
        First we select a set of candidate words using the n-grams index strategy, then we calculate the Levenshtein
        distance of the candidates. The max value for the edit distance is choose by a percentage of the length of the
        word.
        :param ocr_data:
        :param search_terms:
        :param no_relevant_terms: terms that are not relevant and not be considered.
        :param black_list_terms:
        :param max_percentage_error: percentage of the word that can be wrong from 0 to 1.
        :return:

        Units:
        ps.: fraction_error is the error of the found term from 0 to 1, 0 means an exactly match.

        """

        if black_list_terms is None:
            black_list_terms = []

        # Collecting words from the dictionary from orc_data, not using tokenizer for now.
        candidate_words, candidate_boxes = cls.candidate_words_boxes(ocr_data)

        finder_model = FinderGramLevenshtein(candidate_words)
        results_list = []

        for term in search_terms:
            results_finder = finder_model.find_word(
                term, no_relevant_terms=no_relevant_terms, max_percentage_error=max_percentage_error)
            if results_finder is not None:
                indices = results_finder['indices']
                new_term = SearchTerm(value=term)
                for f_term, box, score in zip(
                        results_finder['words'], candidate_boxes[indices], results_finder['distances']):
                    fraction_error = float(np.around(score / len(term), 2))
                    new_term.found_terms.append(
                        FoundTerm(box=Box(**box), value=f_term, score=fraction_error, score_unit="fraction_error")
                    )
                results_list.append(new_term)

        return results_list
