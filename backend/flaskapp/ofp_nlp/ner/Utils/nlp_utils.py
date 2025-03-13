import re

from flaskapp.ofp_nlp.ner.Utils import professions_file


class NlpUtils:

    PROFESSIONS: str = None

    @staticmethod
    def clean_text_from_dot(text: str) -> str:
        """
        This method cleans the text string from unnecessary dots. However, it tries to
        keep it at the end of a phrase, i.e:

        >>> NlpUtils.clean_text_from_dot('This is a ba...d ocr. I will improve it.')
        >>> 'This is a bad ocr. I will improve it.'

        :param text: The text to clean up.
        :return: The new text without unnecessary dots.
        """

        # Remove dots only between lowercase words. ie: o....i -> oi
        s = re.sub(r"(?<=[a-zäüöß])(\.+)(?=[a-zäüöß])", '', text)
        # replace multiple dots between lowercase words and uppercase. ie: o....T -> o. T
        s = re.sub(r"(?<=[a-zäüöß])(\.+)(?=[A-Z])", '. ', s)
        # clean any residual multiple punctuation with more than one dot ande replace by .
        s = re.sub(r"\.+", '.', s)
        return s

    @classmethod
    def clean_up_ocr(cls, text):
        """
        Function to clean OCR text from doube spaces or more, double points or more and weird characters.

        :param text:
        :return:
        """
        # Remove dots only between lowercase words. ie: o....i -> oi
        text = cls.clean_text_from_dot(text)
        text = re.sub(r"[^0-9A-Za-züöäß.\s]", ' ', text)
        # text = re.sub('  +', ' ', text)
        # text = re.sub('\n', ' ', text)
        # text = re.sub('\\s+', ' ', text)
        # text = re.sub('\r', ' ', text)
        # text = re.sub('[' + ''.join(
        #     ['"', '*', '^', '_', '°', '¤', '?', '<', '>', '|', '@', 'ª', '{', '«', '»', '§', '#', '}', '©', '®', '™',
        #      '~', '#', '&','-','/',"'",'\u2022','\u25A0','\u2605']) + ']', '', text)
        return text

    @staticmethod
    def find_dates_in_text(text: str):
        day_pattern = r"([1-9]|[0]\d|[12]\d|[3][0-1])"
        separator_pattern = r"([./,\s-]+)"
        month_pattern_num = r"0?[1-9]|[1][0-2]"
        month_pattern_str = r"J(?:an(?:uar)?|u[nl]i?)" \
                            r"|Fe(?:b(?:ruar)?)?" \
                            r"|M(?:[äa]rz?|ai)" \
                            r"|A(?:pr(?:il)?|ug(?:ust)?)" \
                            r"|Sep(?:tember)?" \
                            r"|Okt(?:ober)?" \
                            r"|(?:Nov|Dez)(?:ember)?"
        year_pattern = r"([12]\d\d\d)"

        date_pattern_1 = r"(?<!\d)" + \
                         f"{day_pattern}{separator_pattern}" \
                         f"({month_pattern_num}|{month_pattern_str}){separator_pattern}{year_pattern}" + \
                         r"(?!\d)"

        # cover cases like: November 1945
        date_pattern_2 = r"(?<!\d)" + \
                         f"({month_pattern_str}){separator_pattern.replace('/','')}{year_pattern}" + \
                         r"(?!\d)"

        date_pattern = re.compile(f"{date_pattern_1}|{date_pattern_2}",
                                  flags=re.RegexFlag.I | re.RegexFlag.M | re.RegexFlag.X)

        return date_pattern.finditer(text)

    @staticmethod
    def __load_data_professions():
        with open(professions_file, 'r') as f:
            # skip header
            next(f)
            line = f.readline()
            if line:
                yield line.split(',')[0]

    @classmethod
    def find_professions(cls, text: str):
        if not cls.PROFESSIONS:
            cls.PROFESSIONS = "|".join(list(cls.__load_data_professions()))

        professions_pattern = re.compile(cls.PROFESSIONS,
                                         flags=re.RegexFlag.I | re.RegexFlag.M | re.RegexFlag.X)
        return professions_pattern.finditer(text)
