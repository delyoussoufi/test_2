from typing import Union, List

import numpy as np

from .finder_gram_levenshtein import FinderGramLevenshtein
from .finder_gram_levenshtein_model import FinderGramLevenshteinModel
from ..data_structure import SearchTerm, FoundTerm, Box
from ..preprocessing.operation.raw_text import RemoveSpecialCharacters
from ..utils import candidate_words_boxes, combine_words_boxes


class FinderGramLevenshteinModelMultiple(FinderGramLevenshteinModel):
    """
    This model include bi-, tri-, n-grams into the candidate words, that means that words such as "B.e.r.l.i.n" will be
    recovered as "Berlin".
    """

    operator_exclude = "-"

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
        :param black_list_terms: list of terms that if present the page will not be classified.
        :param max_percentage_error: percentage of the word that can be wrong from 0 to 1.
        :return: List of Found Terms

        Units:
        ps.: fraction_error is the error of the found term from 0 to 1, 0 means an exactly match.

        """
        if black_list_terms is None:
            black_list_terms = []

        # Collecting words from the dictionary from orc_data, not using tokenizer for now.
        candidate_words, candidate_boxes = cls.preprocessing(ocr_data)

        # New words and Boxes
        candidate_words, candidate_boxes, candidate_intersections = combine_words_boxes(
            candidate_words, candidate_boxes)
        finder_model = FinderGramLevenshtein(candidate_words)

        search_terms_extended = black_list_terms + search_terms

        # Find words with operations: "and" and "-".
        results_list = []
        for term in search_terms_extended:
            multiple_results = []
            multiple_results_operators = []
            operators = []
            terms = term.split()
            for term_i in terms:
                if term_i[0] == cls.operator_exclude:
                    operators.append(cls.operator_exclude)
                    clean_term = term_i[1:]
                else:
                    operators.append(cls.operator_include)
                    clean_term = term_i

                results_finder = finder_model.find_word(
                    clean_term, no_relevant_terms=no_relevant_terms, max_percentage_error=max_percentage_error)

                # Multiple search terms, this is responsible for he and operator of composed terms.
                if results_finder:
                    multiple_results.append(results_finder)
                    multiple_results_operators.append(1)
                else:
                    multiple_results_operators.append(0)

            check_operators = {}
            for operator, number in zip(operators, multiple_results_operators):
                if operator in check_operators:
                    check_operators[operator] += number
                else:
                    check_operators[operator] = number
            operators = np.array(operators)

            # And Operations
            expected_value_include = np.sum(operators == cls.operator_include)
            value_include = check_operators.get(cls.operator_include, 0)
            if value_include != expected_value_include:
                continue

            # - Operation
            expected_value_exclude = 0
            value_exclude = check_operators.get(cls.operator_exclude, 0)
            if value_exclude != expected_value_exclude:
                continue

            # Continue the process.
            results_words = []
            results_indices = []
            results_distances = []
            for results_finder in multiple_results:
                indices = results_finder["indices"]
                scores = results_finder["distances"]
                score_indices = {key: value for key, value in zip(indices, scores)}

                # Competition of words with superposition
                indices_losers = cls.find_losers_candidates_from_superposition(
                    candidate_intersections, indices, score_indices)

                for f_term, index, score in zip(
                        results_finder['words'],
                        indices,
                        results_finder['distances'],
                ):
                    if index not in indices_losers:
                        results_words.append(f_term)
                        results_indices.append(index)
                        results_distances.append(score)

            # Black List Terms.
            if term in black_list_terms:
                # print(f"term: {term} - blacklist: {black_list_terms} - {results_words}")
                return []

            # Final step: create the objects SearchTerm
            new_term = SearchTerm(value=term)
            for f_term, index, score in zip(
                    results_words,
                    results_indices,
                    results_distances,
            ):
                box = candidate_boxes[index]
                fraction_error = float(np.around(score / len(f_term), 2))
                new_term.found_terms.append(
                    FoundTerm(box=Box(**box), value=f_term, score=fraction_error, score_unit="fraction_error")
                )
            results_list.append(new_term)

        return results_list

    operator_include = "+"

    @classmethod
    def preprocessing(cls, ocr_data):
        candidate_words, candidate_boxes = candidate_words_boxes(ocr_data)
        # candidate_words = RemoveSpecialCharacters(
        #     col_name="words",
        #     regular_expression=r"[\:,;!?\";]",
        #     replace_with="",
        #     comment="Remove some special characters and replace with empty string."
        # ).process(dict(words=candidate_words))['words']
        candidate_words = RemoveSpecialCharacters(
            col_name="words",
            regular_expression=r"[\:,;!?\";]",
            replace_with=" ",
            comment="Remove some special characters and replace with empty string."
        ).process(dict(words=candidate_words))['words']
        candidate_words = RemoveSpecialCharacters(
            col_name="words",
            regular_expression=r"\.",
            replace_with=" ",
            comment="Remove points and replace with spaces."
        ).process(dict(words=candidate_words))['words']
        candidate_words = RemoveSpecialCharacters(
            col_name="words",
            regular_expression=r"\s+",
            replace_with=" ",
            comment="Remove multiple whitespaces."
        ).process(dict(words=candidate_words))['words']
        candidate_words = [w.strip() for w in candidate_words]
        return candidate_words, candidate_boxes

    @staticmethod
    def find_losers_candidates_from_superposition(candidate_intersections: np.ndarray, indices, score_indices):
        """
        Given a list of candidates of words that intersect, select the best and return a list of not visible words,
        i.e., a list with the indices of the loser candidate words.

        :param candidate_intersections: a list of candidate words that intersect
        :param indices: indices of the candidate words
        :param score_indices: score of each candidate word
        :return: a list of indices of the losers candidates words
        """
        # TODO Check this change. We get error when candidate_intersections has shape (n, 0)
        if candidate_intersections.size <= 1:
            return []
        intersections_i = candidate_intersections[indices]
        indices_losers = []
        for index, indices_intersection in zip(indices, intersections_i):
            if index not in indices_losers:
                indices_all = [index] + indices_intersection
                scores_all = [score_indices[key] for key in indices_all if key in score_indices]
                winner = np.argmin(scores_all)
                indices_winner = indices_all[winner]
                indices_losers += [e for e in indices_all if e != indices_winner]

        return indices_losers
