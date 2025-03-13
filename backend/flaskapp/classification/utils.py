"""
# CHARACTERS_SUB = {"ü": "u", "ä": "a", "ö": "o"}
"""
import copy
from typing import List, Union

import nltk
import numpy as np


def find_fuzzy_levenshtein_edit_distance(
        word: str,
        word_candidates: List[str],
        select_top=10,
        select_best: Union[float, None] = None,
        return_score=False,
        return_indices=False,
        return_words=True,
        transpositions=False):
    """
    Localize a word in a list of words in a fuzzy approach using the Levenshtein edit distance.
    :param word: to be located among the candidates.
    :param word_candidates: list of words candidates where the search will be performed.
    :param select_top: return the top "select_top" words, if "select_best" is None
    :param select_best: TODO: to implement
    :param return_score: return the levenshtein_edit_distance
    :param return_indices: indices of the found words from word_candidates
    :param return_words: return the found words
    :param transpositions: transposition is consider during calculation of levenshtein_edit_distance
                    see func levenshtein_edit_distance documentation for details
    :return: list of words that were found using levenshtein_edit_distance as a criteria
             if  "return_score" is True return a list of words and levenshtein values.
    """
    distances = []
    word_candidates = np.array(word_candidates)
    if len(word_candidates.shape) == 0:
        return np.empty(shape=0), np.empty(shape=0)
    for word_i in word_candidates:
        distance = levenshtein_edit_distance(word_i, word, transpositions=transpositions)
        distances.append(distance)
    indices = np.argsort(distances)[:select_top]

    results = dict()
    if return_indices:
        results["indices"] = indices
    if return_score:
        results["distances"] = np.array(distances)[indices]
    if return_words:
        results["words"] = word_candidates[indices]
    return results


def jaccard_index_version2(set_1, set_2):
    """
    TODO: There is a subtraction in the norma, not sure which is the best.
    """
    sum_index = 0
    for a in set_1:
        if a in set_2:
            sum_index += 1
    norma = len(set_1) + len(set_2) - sum_index
    return sum_index / norma


def jaccard_index(set_1, set_2):
    sum_index = 0
    for a in set_1:
        if a in set_2:
            sum_index += 2
    norma = len(set_1) + len(set_2)
    return sum_index / norma


def test_jaccard_index():
    print("test_jaccard_index")
    words = [("Test", "Tets"), ("caracter", "character"), ("method", "Metod"), ("method", "metod")]
    for e, ee in words:
        e_mod = "#" + e + "$"
        n_gram_e = n_gram(e_mod, n=3)
        ee_mod = "#" + ee + "$"
        n_gram_ee = n_gram(ee_mod, n=3)
        print(n_gram_e, n_gram_ee)
        print(jaccard_index(n_gram_e, n_gram_ee))


def levenshtein_edit_distance(word: str, another_word: str, transpositions=True, case_insensitive=True) -> int:
    """
    Calculate the Levenshtein edit-distance between two words.
    TODO: substitution_cost can be used together with the length of the word.
    :param word: first word that will be compared
    :param another_word: second word that will be used in the comparison.
    :param transpositions: consider the transposition of characters,
    :param case_insensitive: True to ignore differences between BERLIN and berlin.
    :return: an int of the levenshtein edit distance value between the two words, "word" and "another_word"

    :Example:

     if transpositions=True "Tets" -> "Test" return 1; return 2 otherwise.
    """
    if case_insensitive:
        word = word.lower()
        another_word = another_word.lower()

    return nltk.edit_distance(word, another_word, transpositions=transpositions)


def n_gram(word, n):
    """
    Create a n_gram from a word.
    :param word: a word
    :param n: number of n-grams that will be used.
    :return: a list of n-grams
    """
    return [word[i:i + n] for i in range(len(word) - n + 1)]


def candidate_words_boxes(orc_data: dict):
    """
    Return the list of candidate words and their boxes from a orc_data dictionary.
    """
    words_dicts = orc_data["words"]  # No treating the error, key error will be automatic raised.
    word_list = []
    box_list = []
    for word_dict_i in words_dicts:
        word_list.append(word_dict_i['text'])
        box_list.append(word_dict_i['box'])
    return np.array(word_list), np.array(box_list)


def n_gram_indices(word, n):
    """
    Create a n_gram from a word with indices.
    :param word: a word
    :param n: number of n-grams that will be used.
    :return: a list of n-grams
    """
    solution = [(list(range(i, i + n)), "".join(word[i:i + n])) for i in range(len(word) - n + 1)]
    if solution:
        indices, words = zip(*solution)
        return indices, words
    return None


def combine_words_boxes(words, boxes, n_max=10, min_size_word=4, max_size_word=20):
    """
    Combining close words to generate new list of words and boxes.
    This routine is used when the ocr gives a word such as "B e r l i n",
    then this routine recover the word "Berlin".
    Note: Average size of words in German 8.25
    :param words:
    :param boxes:
    :param n_max:
    :param min_size_word:
    :param max_size_word:
    :return:
    """
    generated_words_all = []
    generated_boxes_all = []
    generated_indices_all = []  # This indices are based in the whole set of words.
    generated_intersect_all = []
    intersections_all = dict()
    count_indices = IndicesWordSegments()

    # Go through all words and box and generate new words based on the spaces inside the word.
    for i, (word, box) in enumerate(zip(words, boxes)):
        generated_words = []
        generated_boxes = []
        generated_indices = []  # This indices are based in the whole set of words.

        complete_list_words, complete_list_indices, max_len_words_sep, len_words_sep = create_words(
            word, separator=" ", n_max=n_max, average_size_words=max_size_word)

        # Create a New list with the correct indices, the index is created for each segment of the token.
        new_complete_list_indices = []  # new set of indices unique over the whole set of words.
        for indices in complete_list_indices:
            new_complete_list_indices.append(count_indices.update_index(indices))

        # Creating Boxes
        # TODO check when len(word)=0
        delta_box = (box["xf"] - box['x0']) / max(len(word), 1)  # division by zero can happen here.
        for word_c, indices_c, n_indices in zip(complete_list_words, complete_list_indices, new_complete_list_indices):

            if len(word_c) > max_len_words_sep or len(word_c) < min_size_word:
                continue
            # print(word_c)
            new_box = copy.copy(box)
            new_box["x0"] = np.round(np.sum(len_words_sep[:indices_c[0]]) * delta_box + new_box["x0"], 4)
            new_box["xf"] = np.round(np.sum(len_words_sep[indices_c]) * delta_box + new_box["x0"], 4)
            generated_words.append(word_c)
            generated_boxes.append(new_box)
            new_indices = count_indices.transform(n_indices)
            generated_indices.append(new_indices)

        # Finding intersections between words
        len_generated = len(generated_indices_all)
        intersections = {i+len_generated: [] for i in range(len(generated_indices))}

        for i in range(len(generated_indices)):
            for j in range(i + 1, len(generated_indices)):
                intersect = np.intersect1d(generated_indices[i], generated_indices[j])
                if len(intersect):
                    jj = j + len_generated
                    ii = i + len_generated
                    intersections[ii].append(jj)
                    intersections[jj].append(ii)
                    generated_intersect_all.append([i+len_generated, j+len_generated])

        generated_words_all.extend(generated_words)
        generated_boxes_all.extend(generated_boxes)
        generated_indices_all.extend(generated_indices)
        intersections_all.update(intersections)

    intersections_all = list(intersections_all.values())
    return np.array(generated_words_all), np.array(generated_boxes_all, dtype=object), np.array(intersections_all,
                                                                                                dtype=object)


class IndicesWordSegments:
    """
    Generate new indices for segments of words in a token. Each segment has a unique index value.
    This class is used in the combine_words_boxes routine.
    """

    def __init__(self):
        self.indices = {}
        self.i = 0

    def transform(self, values: List):
        """
        Transform a positional index into a segment index.
        :param values: a list with the positional indices
        :return: new segment indices
        """
        new_values = []
        for value in values:
            if value in self.indices:
                new_values.append(self.indices[value])
            else:
                self.i += 1
                self.indices[value] = self.i
                new_values.append(self.indices[value])
        return new_values

    def update_index(self, values: List):
        """
        Update a positional indices with the current index value.
        :param values: a list with the positional indices
        :return: list with the segment indices
        """
        return [e + self.i for e in values]


def create_words(word, separator=" ", n_max=10, average_size_words=20):
    """
    Routine used in the combine_words_boxes to generate a set of new words.
    """
    words_sep = word.split(separator)
    len_words_sep = np.array([len(w) + 1 for w in words_sep])
    len_words_sep[-1] -= 1
    max_len_words_sep = np.max([average_size_words, np.max(len_words_sep)])

    # Combining close words.
    complete_list_words = []
    complete_list_indices = []
    for n in range(1, n_max):
        results = n_gram_indices(words_sep, n)
        if results is None:
            break
        indices, new_words = results
        complete_list_words.extend(new_words)
        complete_list_indices.extend(indices)

    return complete_list_words, complete_list_indices, max_len_words_sep, len_words_sep


def box_intersection(box1, box2):
    """
    Verify if to boxes are intersecting each other
    :param box1:
    :param box2:
    :return: True if there is intersection and False otherwise.
    """
    a_x = box1["x0"] + box1["xf"] / 2.
    b_x = box2["x0"] + box2["xf"] / 2.
    box_w = box1["xf"] + box2["xf"]
    a_y = box1["y0"] + box1["yf"] / 2.
    b_y = box2["y0"] + box2["yf"] / 2.
    box_h = box1["yf"] + box2["yf"]
    return (abs(a_x - b_x) * 2 < box_w) & (abs(a_y - b_y) * 2 < box_h)


def test_box_intersection():
    box1 = {'x0': 0.0, 'xf': 0.7058823529411764, 'y0': 0.5, 'yf': 1.5}
    box2 = {'x0': 0.7158823529411765, 'xf': 1.1176470588235294, 'y0': 0.5, 'yf': 1.5}
    assert box_intersection(box1, box2), False


def test_combine_words_boxes():
    words = ["Berlin Schö neberg d6 Se pt em bLr", "casa", "B e r l in"]
    boxes = np.array([{'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                      {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0},
                      {'x0': 0.0, 'xf': 2.0, 'y0': 0.0, 'yf': 1.0}
                      ])
    generated_words, generated_boxes, generated_indices = combine_words_boxes(words, boxes)
    for e, ee, eee in zip(generated_words, generated_boxes, generated_indices):
        print(e, ee, eee)


if __name__ == "__main__":
    test_combine_words_boxes()
