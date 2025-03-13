import unittest

from flaskapp.http_util.mapper import MapAttributes


class TestMapAttributes(unittest.TestCase):
    def test_map_to_ts_style(self):
        test_cases = (
            ('target_folder_id', 'targetFolderId'),
            ('id', 'id'),
            ('folder_id', 'folderId'),
            ('expected_images', 'expectedImages'),
        )
        for value, expected in test_cases:
            self.assertEqual(expected, MapAttributes.map_to_ts_style(value))

    def test_map_to_py_style(self):
        test_cases = (
            ('targetFolderId', 'target_folder_id'),
            ('id', 'id'),
            ('folderId', 'folder_id'),
            ('expectedImages', 'expected_images'),
            ('folder_id', 'folder_id'),
        )
        for value, expected in test_cases:
            self.assertEqual(expected, MapAttributes.map_to_py_style(value))


if __name__ == '__main__':
    unittest.main()
