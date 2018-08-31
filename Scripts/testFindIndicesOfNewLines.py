import unittest

from findNewlineIndices import find_indices_of_new_lines


class TestFindIndicesOfNewLines(unittest.TestCase):

    def test_find_single_index(self):
        string = '012\n456'

        actual_indices = find_indices_of_new_lines(string)

        expected_indices = [3]
        self.assertEqual(expected_indices, actual_indices)

    def test_find_multiple_indices(self):
        string = '012\n45\n7'

        actual_indices = find_indices_of_new_lines(string)

        expected_indices = [3, 6]
        self.assertEqual(expected_indices, actual_indices)

    def test_find_starting_newline(self):
        string = '\n1234567'

        actual_indices = find_indices_of_new_lines(string)

        expected_indices = [0]
        self.assertEqual(expected_indices, actual_indices)

    def test_find_ending_newline(self):
        string = '0123\n'

        actual_indices = find_indices_of_new_lines(string)

        expected_indices = [4]
        self.assertEqual(expected_indices, actual_indices)