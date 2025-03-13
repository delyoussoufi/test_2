

class NumberUtils:

    @staticmethod
    def is_integer(str: str) -> bool:
        """
        Tests if a string is an integer number.
        :param str: The string to be tested.
        :return: True, if the string is an integer
        """
        try:
            int(str)
            return True
        except ValueError:
            return False

    @staticmethod
    def left_pad_string_with_zeros(str: str, number_of_digits: int) -> str:
        """
        Pad the given string with zeros on left side.
        :param str: the string to be padded.
        :param number_of_digits: how many digits it should have. (i.e str = 1, size = 4, result = 0001).
        :return: The padded string with zeros.
        """
        if not str or str == "":
            return ""

        result = ""
        digits = ""
        found = False

        for i, char in enumerate(str):
            if char.isdigit():
                if i > 0 and not found:
                    result += str[0:i]
                digits += char
                found = True
                if i == len(str) - 1:
                    result += NumberUtils.build_filling_string(digits, number_of_digits)
            elif found:
                result += NumberUtils.build_filling_string(digits, number_of_digits)
                if i < len(str):
                    result += str[i:len(str)]
                break

        return result

    @staticmethod
    def build_filling_string(digits: str, filling: int) -> str:
        filling_string = ""
        if len(digits) < filling:
            i = 0
            while i < filling - len(digits):
                i += 1
                filling_string += "0"
        filling_string += digits
        return filling_string
