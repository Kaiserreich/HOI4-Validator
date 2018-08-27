import unittest

from checkEvents import find_end_index


class TestFindEndIndex(unittest.TestCase):

    def test_single_pair(self):
        string = '0 = {5678}'
        start_index = 0

        actual_end_index = find_end_index(string, start_index)

        expected_end_index = 9
        self.assertEqual(expected_end_index, actual_end_index)

    def test_interior_scope(self):
        string = '0{23{5}7}'
        start_index = 0

        actual_end_index = find_end_index(string, start_index)

        expected_end_index = 8
        self.assertEqual(expected_end_index, actual_end_index)

    def test_start_index_after_brackets(self):
        string = '0{}3{567}'
        start_index = 3

        actual_end_index = find_end_index(string, start_index)

        expected_end_index = 8
        self.assertEqual(expected_end_index, actual_end_index)
