import unittest

from removeComments import remove_comments


class TestRemoveComments(unittest.TestCase):

    def test_standard_case(self):
        line = '1234 #56789\n'

        actual_result = remove_comments(line)

        expected_result = '1234 \n'
        self.assertEqual(expected_result, actual_result)

    def test_all_comments(self):
        line = '#1234\n'

        actual_result = remove_comments(line)

        expected_result = '\n'
        self.assertEqual(expected_result, actual_result)

    def test_multiple_hashtags(self):
        line = '123###########\n'

        actual_result = remove_comments(line)

        expected_result = '123\n'
        self.assertEqual(expected_result, actual_result)

    def test_multiple_lines(self):
        string = '123#456\n789#\n'

        actual_result = remove_comments(string)

        expected_result = '123\n789\n'
        self.assertEqual(expected_result, actual_result)
