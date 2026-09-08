from flashtext import KeywordProcessor
import logging
import unittest

logger = logging.getLogger(__name__)

class TestPublicKPDictionaryLikeFeatures(unittest.TestCase):
    def setUp(self):
        logger.info("Starting public dict-like tests...")

    def tearDown(self):
        logger.info("Ending public dict-like tests.")

    def test_term_in_dictionary_public(self):
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keyword('ml', 'MachineLearning')
        keyword_processor.add_keyword('colourful', 'colorful')
        keyword_processor.get_keyword('ml')
        self.assertEqual(keyword_processor.get_keyword('ml'),
                         'MachineLearning',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['colourful'],
                         'colorful',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['Unknown'],
                         None,
                         "get_keyword didn't return expected Keyword")
        self.assertTrue('colourful' in keyword_processor,
                        "get_keyword didn't return expected Keyword")
        self.assertFalse('Unknown' in keyword_processor,
                         "get_keyword didn't return expected Keyword")

    def test_term_in_dictionary_case_sensitive_public(self):
        keyword_processor = KeywordProcessor(case_sensitive=True)
        keyword_processor.add_keyword('ml', 'MachineLearning')
        keyword_processor.add_keyword('colourful', 'colorful')
        keyword_processor.get_keyword('ml')
        self.assertEqual(keyword_processor.get_keyword('ml'),
                         'MachineLearning',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['colourful'],
                         'colorful',
                         "get_keyword didn't return expected Keyword")
        self.assertEqual(keyword_processor['ML'],
                         None,
                         "get_keyword didn't return expected Keyword")
        self.assertTrue('colourful' in keyword_processor,
                        "get_keyword didn't return expected Keyword")
        self.assertFalse('Colourful' in keyword_processor,
                         "get_keyword didn't return expected Keyword")

if __name__ == '__main__':
    unittest.main()