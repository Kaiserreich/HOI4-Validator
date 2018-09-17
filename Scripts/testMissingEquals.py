import unittest
from checkMissingEquals import missing_equals_gen


class TestMissingAliveCheckGen(unittest.TestCase):

    def test_valid_alive_check(self):
        string = 'if = {\nlimit = { country_exists = ITA }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual([], bugs)

    def test_missing_top_level(self):
        string = 'diplomatic_relation  { country = ITA }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(1, len(bugs))

    def test_missing_inner_scope(self):
        string = 'diplomatic_relation = { country  ITA }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(1, len(bugs))

    def test_right_line(self):
        string = 'if = {\nlimit = { country_exists  ITL }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(2, bugs[0].line)

    def test_multiple_missing(self):
        string = 'if  {\nlimit = { country_exists  ITL }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(2, len(bugs))

    def test_greater_than(self):
        string = 'if = {\nlimit = { country_exists < ITL }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_no_space_after_leading_bracket(self):
        string = 'country_event = {id = ukr days = 7}'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_string_present(self):
        string = 'create_unit = \"field = contents field = contents\"'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_nested_string_with_space(self):
        string = 'create_unit = \"field = \\\"sub contents\\\" field = contents\"'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_list_of_numbers(self):
        string = 'field = { 123 456 789 }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_list_of_strings(self):
        string = 'field = { \"a\" \"b\" \"c\" }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_tab_after_quotes(self):
        string = 'spriteType = { name = "content"\ttextureFile = content }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_list_of_directions(self):
        string = 'drag_scroll = { left right middle }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))

    def test_list_of_traits(self):
        string = 'traits = { old_guard career_officer offensive_doctrine }'

        bugs = [bug for bug in missing_equals_gen(string, 'test')]

        self.assertEqual(0, len(bugs))