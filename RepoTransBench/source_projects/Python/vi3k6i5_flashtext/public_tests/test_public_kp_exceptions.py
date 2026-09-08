import unittest
from flashtext import KeywordProcessor

class TestPublicKPExceptions(unittest.TestCase):
    def test_public_add_empty_keyword(self):
        kp = KeywordProcessor()
        # Adding an empty string as keyword should fail
        with self.assertRaises(Exception):
            kp.add_keyword('', 'value')

    def test_public_add_empty_clean_name(self):
        kp = KeywordProcessor()
        # Adding empty clean name is fine, but should be found as empty
        kp.add_keyword('new', '')
        self.assertEqual(kp['new'], '')

if __name__ == '__main__':
    unittest.main()