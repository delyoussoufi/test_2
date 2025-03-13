import unittest

from flaskapp.utils import StringUtils


class TestStringUtils(unittest.TestCase):

    def test_extract_signature_number(self):
        test_cases = [
            ['36A (II) 45666-1', 45666],
            ['36 A (II) 45666-1', 45666],
            ['36a (II)  45666/145', 45666],
            ['36b (II)  45666/145', 45666],
            ['36 (II)  45666 / 145', 45666],
            ['2 Kurmärkische Kammer K 78 B', 78],
            ['10B Heiligengrabe AK 21 B', 21],
            ['2A I Kom 12', 12],
            ['AA', 0],
        ]
        for signature, expected in test_cases:
            v = StringUtils.extract_signature_number(signature)
            self.assertEqual(expected, v)

    def test_extract_signature_reference(self):
        test_cases = [
            ['36A (II) 45666', '45666'],
            ['36A (II) 45666-1', '45666-1'],
            ['36 A (II) 45666-1', '45666-1'],
            ['36a (II)  45666/145', '45666/145'],
            ['36b (II)  45666/145', '45666/145'],
            ['36 (II)  45666 / 145', '45666 / 145'],
            ['2 Kurmärkische Kammer K 78 B', '78 B'],
            ['10B Heiligengrabe AK 21 B', '21 B'],
            ['AA', 'AA'],
        ]
        for signature, expected in test_cases:
            v = StringUtils.extract_signature_reference(signature)
            self.assertEqual(expected, v)


if __name__ == '__main__':
    unittest.main()
