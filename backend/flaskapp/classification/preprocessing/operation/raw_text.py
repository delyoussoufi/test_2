import re
from typing import Dict

from dataline import Operation


class RemoveSpecialCharacters(Operation):
    """
    Remove Special character from each row of the data.
    Uses a regular expression using re.
    """
    def __init__(self, col_name: str, regular_expression: str, replace_with: str = " ",  comment: str = "", **kwargs):
        super().__init__(**kwargs)
        self.col_name = col_name
        self.regular_expression = regular_expression
        self.replace_with = replace_with
        self.comment = comment

    def process(self, data: Dict) -> Dict:
        self.report["Comment"] = self.comment
        self.report["Regular expression used"] = self.regular_expression
        self.report["Replaced with"] = self.replace_with
        if len(data[self.col_name]):
            number_characters_per_instance = map(lambda x: len(re.sub(" ", "", x)), data[self.col_name])
            values = map(lambda x: re.subn(self.regular_expression, self.replace_with, x), data[self.col_name])
            new_values, n_subs = zip(*values)
            data[self.col_name] = list(new_values)
            self.report["Number of replacements per instance"] = list(n_subs)
            total_removal = sum(list(n_subs))
            total_initial = sum(list(number_characters_per_instance))
            self.report["Total number of characters removed"] = total_removal
            self.report["Initial number of character"] = total_initial
            self.report["Final number of character"] = total_initial - total_removal
            # TODO division by 0 can happen here.
            self.report["Fraction of characters removed"] = total_removal / max(1., total_initial)
        else:
            self.report["Empty List"] = ""
            self.report["Number of replacements per instance"] = 0
            self.report["Total number of characters removed"] = 0
            self.report["Initial number of character"] = 0
            self.report["Final number of character"] = 0
            self.report["Fraction of characters removed"] = 0

        return data


class RemoveLeftRightSpace(Operation):
    """
    Remove spaces on the right and left of words.
    """
    def __init__(self, col_name: str, **kwargs):
        """
        :param col_name: column that the operation will be applied.
        """
        super().__init__(**kwargs)
        self.col_name = col_name

    def process(self, data: Dict) -> Dict:
        print(data[self.col_name])
        values = [w.strip() for w in data[self.col_name]]
        print(values)
        data[self.col_name] = values
        return data


class CombineWords(Operation):
    """
    Combine words that are separated by space.
    """
    def __init__(self, col_name: str, box_col_name: str, separator: str = " ", comment: str = "", **kwargs):
        super().__init__(**kwargs)
        self.col_name = col_name
        self.box_col_name = box_col_name
        self.separator = separator
        self.comment = comment

    def process(self, data: Dict) -> Dict:
        # TODO redo method.
        pass
        # self.report["Comment"] = self.comment
        # self.report["separator"] = self.separator
        # number_characters_per_instance = map(lambda x: len(re.sub(" ", "", x)), data[self.col_name])
        #
        # for word, box in zip(data[self.col_name], data[self.box_col_name]):
        #     words_sep = word.split(self.separator)
        #     size_box = box["xf"] - box['x0']
        #     new_words = combinations(words_sep)
        #
        #
        #
        # values = map(lambda x: x.split(self.separator), )
        # data[self.col_name] = values
        # self.report["Number of replacements per instance"] = list(n_subs)
        # total_removal = sum(list(n_subs))
        # total_initial = sum(list(number_characters_per_instance))
        # self.report["Total number of characters removed"] = total_removal
        # self.report["Initial number of character"] = total_initial
        # self.report["Final number of character"] = total_initial-total_removal
        # self.report["Fraction of characters removed"] = total_removal/total_initial

        # return data
