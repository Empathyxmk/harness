from flashtext import KeywordProcessor
import logging
import unittest

logger = logging.getLogger(__name__)

class TestPublicExtractFuzzy(unittest.TestCase):
    def setUp(self):
        logger.info("Starting public fuzzy test...")

    def tearDown(self):
        logger.info("Ending public fuzzy test.")

    def test_extract_deletion_public(self):
        # Fuzzy deletion with different keyword and typo
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('telegram', 'chatapp')
        sentence = "connect using telegrm now"
        extracted_keywords = [('chatapp', 16, 23)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)

    def test_extract_addition_public(self):
        # Fuzzy addition with different data
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('favorite color', 'couleur favorite')
        keyword_proc.add_keyword('favorite place', 'lieu favori')
        sentence = "favourite color and favorite pllace"
        extracted_keywords = [('couleur favorite', 0, 15), ('lieu favori', 21, 36)]
        self.assertListEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)

    def test_correct_keyword_on_addition_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('favorite color', 'couleur favorite')
        keyword_proc.add_keyword('favorite place', 'lieu favori')

        current_dict = keyword_proc.keyword_trie_dict['f']['a']['v']['o']
        closest_node, cost, depth = next(
            keyword_proc.levensthein('ur', max_cost=1, start_node=current_dict),
            ({}, 0, 0)
        )
        self.assertDictEqual(closest_node, current_dict['r']['i'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 2)

        current_dict_continued = {'l': {'a': {'c': {'e': {'_keyword_': 'lieu favori'}}}}}
        closest_node, cost, depth = next(
            keyword_proc.levensthein('ace', max_cost=1, start_node=current_dict_continued),
            ({}, 0, 0)
        )
        self.assertDictEqual(closest_node, current_dict_continued['l']['a']['c']['e'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 3)

    def test_correct_keyword_on_deletion_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('telegram')
        current_dict = {'e': {'g': {'r': {'a': {'m': {'_keyword_': 'telegram'}}}}}}
        closest_node, cost, depth = next(
            keyword_proc.levensthein('gram', max_cost=1, start_node=current_dict),
            ({}, 0, 0)
        )
        self.assertDictEqual(closest_node, current_dict['e']['g']['r']['a']['m'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 5)

    def test_correct_keyword_on_substitution_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('telegram', 'chatapp')
        current_dict = keyword_proc.keyword_trie_dict['t']['e']
        closest_node, cost, depth = next(
            keyword_proc.levensthein('legrum', max_cost=1, start_node=current_dict),
            ({}, 0, 0)
        )
        self.assertDictEqual(closest_node, current_dict['l']['e']['g']['r']['a']['m'])
        self.assertEqual(cost, 1)
        self.assertEqual(depth, 6)

    def test_extract_cost_spread_over_multiple_words_public(self):
        keyword_proc = KeywordProcessor()
        keyword_made_of_multiple_words = 'collection of various terms'
        keyword_proc.add_keyword(keyword_made_of_multiple_words)
        sentence = "find the colllection of vrious terms easily"

        extracted_keywords = [(keyword_made_of_multiple_words, 9, 36)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), extracted_keywords)

    def test_extract_multiple_keywords_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('main concept')
        keyword_proc.add_keyword('another topic')
        sentence = "focus on main concpt and then go to anotherr topic"
        extracted_keywords = [
            ('main concept', 9, 21),
            ('another topic', 38, 51),
        ]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), extracted_keywords)

    def test_intermediate_match_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('central idea')
        keyword_proc.add_keyword('central idea in books')
        sentence = "This book explains the cenral idea in boooks"

        shortest_keyword = ('central idea', 23, 35)
        longest_keyword = ('central idea in books', 23, 46)
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), [longest_keyword])
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=1), [shortest_keyword])

    def test_intermediate_match_then_no_match_public(self):
        keyword_proc = KeywordProcessor()
        keyword_proc.add_keyword('concept')
        keyword_proc.add_keyword('concept with examples')
        sentence = "First, check the concpt with examples available, later concept will be revised"
        keywords = [('concept', 17, 23), ('concept', 57, 64)]
        self.assertEqual(keyword_proc.extract_keywords(sentence, span_info=True, max_cost=2), keywords)

if __name__ == '__main__':
    unittest.main()