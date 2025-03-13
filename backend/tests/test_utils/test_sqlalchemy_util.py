import unittest
from flaskapp.utils import parse_to_ts_query_string


class TestSqlalchemyUtil(unittest.TestCase):
    def test_parse_to_ts_query_string(self):

        test_cases = (
            ('Cahen* M & Margarete', 'Cahen:* | M & Margarete'),
            ('Cahen M & Margar* L M', 'Cahen | M & Margar:* | L | M'),
            ('Cahen M Margarete', 'Cahen | M | Margarete'),
            ('Cahen Margarete', 'Cahen | Margarete'),
            ('Cahen & Margarete & M', 'Cahen & Margarete & M'),
            ('Cahen <-> Margarete', 'Cahen<->Margarete'),
            ('Cahen<->Margarete & M', 'Cahen<->Margarete & M'),
            ('Cah* <-> Margarete & M', 'Cah:*<->Margarete & M'),
        )
        for value, expected in test_cases:
            self.assertEqual(expected, parse_to_ts_query_string(value))


if __name__ == '__main__':
    unittest.main()
