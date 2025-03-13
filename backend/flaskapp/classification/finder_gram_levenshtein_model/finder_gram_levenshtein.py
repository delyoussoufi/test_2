"""
Strategies: n-gram overlap and the Levenshtein distance strategies.

This strategy to not consider the position of the n-grams, it consider in some level but not implicit.

"""
# TODO: Possible future developments:
#  1. The OCR have a score of how confidence it is about the detection of words and characters.
#  Use the confidence from OCR to increase the accepted error from find the word. If the confidence of the OCR
#  is small the accepted error should be higher.
#  2. Use the distance of the neighbor words. Physical distance image, in the JSON file, we have the position each word
#  available.

from collections import Counter
from typing import Dict, Union, List, Sequence

import numpy as np

from ..utils import n_gram, find_fuzzy_levenshtein_edit_distance


class FinderGramLevenshtein:
    """
    Class to generate and find from a list of words using n-grams and Levenshtein edit distance strategy.

    Methods
    -------

    as_dict()
        return a dictionary of the index grams

    find_using_grams_index(word, max_size_difference=2, select_top=10, select_best=None, return_counter=False)
        return a list of words ranked by n-grams similarities strategy

    find_word(word, select_top=10, select_best=None, return_levenshtein_distance=False, **parameters)
        return a list of words ranked by a combination of n-grams similarities and Levenshtein edit distance strategy

    """

    def __init__(self, word_list: Sequence, n: int = 3, pre: str = "#", pos: str = "$"):
        """
        :param word_list: corpus as a list of words, this can be obtained by a tokenization of corpus.
        :param n: number of grams to be constructed.
        :param pre: prefix used for the begin of a word.
        :param pos: postfix used for the end of a word.
        """
        self.pre = pre
        self.pos = pos
        self.n = n
        self.word_list = np.array(word_list)
        self._index = self._generate_index()

    def as_dict(self):
        return self._index

    def _generate_index(self) -> Dict:
        """
        Generate a gram index to fast search of words that contain such a gram.
        :return: the dictionary where the key are the grams and the values are list of words.
        """
        indices_dict = {}
        for i, word in enumerate(self.word_list):
            word_mod = self.pre + word.lower() + self.pos
            n_grams_word = n_gram(word_mod, self.n)
            for gram in n_grams_word:
                if gram in indices_dict:
                    indices_dict[gram].append(i)
                else:
                    indices_dict[gram] = [i]
        return indices_dict

    def find_using_grams_index(
            self,
            word: str,
            max_size_difference: int = 2,
            select_top: int = 10,
            select_best: Union[float, None] = None,
            return_counter=False,
            return_indices=False,
            return_words=True
    ):
        """
        Find similar words based in an n-grams strategy, e.g., comparing fragments of the words.
        :param word: to find in the GramIndex
        :param max_size_difference: max size difference between the "word" and the list of candidate words
        :param select_top: select the top n words from the candidates, if "select_best" is None
        :param select_best: a float from 0. to 1.0, select criteria based on a selected fraction of the best candidate.
                         It will have priority over "select_top"
        :param return_counter:  return the counter of equal grams
        :param return_indices: return the internal indices of the words
        :param return_words: return the found words
        :return: List of similar words with "word"
        """
        word_mod = self.pre + word.lower() + self.pos
        n_gram_word = n_gram(word_mod, self.n)
        selected_indices = []
        for gram_i in n_gram_word:
            indices_found = self._index.get(gram_i, None)
            if indices_found is not None:
                indices_likely = [
                    idx for idx in indices_found if abs(len(word) - len(self.word_list[idx])) <= max_size_difference]
                selected_indices.extend(indices_likely)
        count_selected_indices = Counter(selected_indices)

        if select_best:
            _, best_score = count_selected_indices.most_common(1)[0]
            results_indices = [
                (word_idx, score) for word_idx, score in count_selected_indices.most_common(100)
                if score > best_score * select_best]
        else:
            results_indices = count_selected_indices.most_common(select_top)

        results = dict()
        if return_counter:
            results["counter"] = np.array([score for _, score in results_indices])
        if return_indices:
            results["indices"] = np.array([i for i, _ in results_indices])
        if return_words:
            results["words"] = np.array([self.word_list[idx] for idx, _ in results_indices])

        return results

    def find_word(
            self, word: str,
            max_percentage_error=0.2,
            no_relevant_terms: Union[List[str], None] = None,
            select_top: int = 10,
            select_best: Union[float, None] = None,
            max_size_difference: int = 2
    ) -> Union[Dict, None]:
        """
        Find words in a fuzzy way, this strategy is a combination of n-grams search and levenshtein edit distance.
        First we select a set of candidate words using the n-grams index strategy, then we calculate the Levenshtein
        distance of the candidates.
        :param word: to be located among the candidate list of words.
        :param max_percentage_error: accepted percentage error of the word.
        :param no_relevant_terms: terms that are not relevant and not be considered.
        :param select_top: select the top n words from the candidates, if "select_best" is None
        :param select_best: see find_using_grams_index documentation
        :param max_size_difference: TODO
        :return: a dictionary with the results of the search
                 or None if no word was found according with the given criteria
             dict(
                indices=indices,
                distances=distances,
                words=words
             )
        """
        if no_relevant_terms is None:
            no_relevant_terms = []
        max_edit_distance = int(len(word) * max_percentage_error)
        result_find_grams = self.find_using_grams_index(
            word,
            return_indices=True,
            return_words=False,
            return_counter=False,
            max_size_difference=max_size_difference)
        indices_word_candidates = result_find_grams["indices"]
        if len(indices_word_candidates) == 0:
            return None
        word_candidates = self.word_list[indices_word_candidates]
        results_edit = find_fuzzy_levenshtein_edit_distance(
            word,
            word_candidates,
            select_top, select_best,
            return_indices=True,
            return_words=True,
            return_score=True)
        indices = indices_word_candidates[results_edit["indices"]]
        distances = results_edit["distances"]
        words = results_edit["words"]
        # Conditions for final selection of words, indices, etc.
        mask_max_distance = distances <= max_edit_distance
        mask_no_relevant = np.array([w not in no_relevant_terms for w in words])
        conditions = mask_max_distance & mask_no_relevant
        # Select from conditions
        distances = distances[conditions]
        indices = indices[conditions]
        words = words[conditions]

        if len(indices):
            return dict(
                indices=indices,
                distances=distances,
                words=words
            )
        return None
