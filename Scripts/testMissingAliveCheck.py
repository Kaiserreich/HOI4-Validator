import unittest
from checkAliveCheck import missing_alive_check_gen


class TestMissingAliveCheckGen(unittest.TestCase):

    def test_valid_alive_check(self):
        string = 'if = {\nlimit = { country_exists = ITA }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_alive_check_gen(string, 'test')]

        self.assertEqual([], bugs)

    def test_unenclosed_diplo_rel(self):
        string = 'diplomatic_relation = { country = ITA }'

        bugs = [bug for bug in missing_alive_check_gen(string, 'test')]

        self.assertEqual(1, len(bugs))

    def test_enclosing_scope_not_an_if(self):
        string = 'effect = {\nlimit = { country_exists = ITA }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_alive_check_gen(string, 'test')]

        self.assertEqual(1, len(bugs))

    def test_check_for_wrong_country(self):
        string = 'if = {\nlimit = { country_exists = ITL }\ndiplomatic_relation = { country = ITA }\n}'

        bugs = [bug for bug in missing_alive_check_gen(string, 'test')]

        self.assertEqual(1, len(bugs))
