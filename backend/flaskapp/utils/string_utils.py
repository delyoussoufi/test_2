import re


class StringUtils:

    EXTRACT_SIGNATURE_NUMBER_PATTERN = r"(^[0-9]+\D+)|(\D+[0-9]*)"

    @staticmethod
    def is_whitespace(string_value: str) -> bool:
        if not string_value:
            return False
        for ch in string_value:
            if not ch.isspace():
                return False
        return True

    @classmethod
    def extract_signature_number(cls, signature: str) -> int:
        try:
            return int(re.sub(re.compile(cls.EXTRACT_SIGNATURE_NUMBER_PATTERN,
                                         flags=re.RegexFlag.IGNORECASE), '', signature))
        except ValueError:
            return 0

    @classmethod
    def extract_signature_reference(cls, signature: str) -> str:
        """
        This method extract tries to extract the second part of signatur, i.e:
            36A (II) 45666/12 -> 45666/12

        :param signature:
        :return:
        """
        try:
            return re.sub(re.compile(r"^(\d+\D+)", flags=re.RegexFlag.IGNORECASE), '', signature).strip()
        except ValueError:
            return f"{cls.extract_signature_number(signature)}"
