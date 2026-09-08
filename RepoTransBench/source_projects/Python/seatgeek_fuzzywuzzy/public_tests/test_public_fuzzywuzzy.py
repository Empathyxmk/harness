# -*- coding: utf8 -*-
from __future__ import unicode_literals
import unittest
import re
import sys
import pycodestyle

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzywuzzy import utils
from fuzzywuzzy.string_processing import StringProcessor

if sys.version_info[0] == 3:
    unicode = str


class PublicStringProcessingTest(unittest.TestCase):
    def test_replace_non_letters_non_numbers_with_whitespace_public(self):
        strings = ["san francisco giants@los angeles dodgers", "São Tomé",
                   "Big City ^^^^^ Giants $$$", "¿Cómo estás?"]
        for string in strings:
            proc_string = StringProcessor.replace_non_letters_non_numbers_with_whitespace(string)
            regex = re.compile(r"(?ui)[\W]")
            for expr in regex.finditer(proc_string):
                self.assertEqual(expr.group(), " ")

    def test_dont_condense_whitespace_public(self):
        s1 = "san francisco giants @ los angeles dodgers"
        s2 = "san francisco giants los angeles dodgers"
        p1 = StringProcessor.replace_non_letters_non_numbers_with_whitespace(s1)
        p2 = StringProcessor.replace_non_letters_non_numbers_with_whitespace(s2)
        self.assertNotEqual(p1, p2)

class PublicUtilsTest(unittest.TestCase):
    def setUp(self):
        self.s1 = "san francisco giants"
        self.s1a = "san francisco giants"
        self.s2 = "SAN FRANCISCO GIANTS"
        self.s3 = "the incredible san francisco giants"
        self.s4 = "san francisco giants vs los angeles dodgers"
        self.s5 = "los angeles dodgers vs san francisco giants"
        self.s6 = "san francisco giants @ los angeles dodgers"
        self.mixed_strings = [
            "The quick brown fox jumps over the lazy dog!",
            "Bonjour tout le monde",
            "¿Cómo estás?",
            "São Tomé",
            "\xacCamarões grelhados",
            "a\xac\u1234\u20ac\U00008000",
            "\u00C5"
        ]
    def tearDown(self):
        pass

    def test_asciidammit_public(self):
        for s in self.mixed_strings:
            utils.asciidammit(s)

    def test_asciionly_public(self):
        for s in self.mixed_strings:
            s = utils.asciidammit(s)
            utils.asciionly(s)

    def test_fullProcess_public(self):
        for s in self.mixed_strings:
            utils.full_process(s)

    def test_fullProcessForceAscii_public(self):
        for s in self.mixed_strings:
            utils.full_process(s, force_ascii=True)

class PublicRatioTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "san francisco giants"
        self.s1a = "san francisco giants"
        self.s2 = "SAN FRANCISCO GIANTS"
        self.s3 = "the incredible san francisco giants"
        self.s4 = "san francisco giants vs los angeles dodgers"
        self.s5 = "los angeles dodgers vs san francisco giants"
        self.s6 = "san francisco giants @ los angeles dodgers"
        self.s7 = 'san francisco city giants @ los angeles dodgers'
        self.s8 = '['
        self.s8a = '['
        self.s9 = '[b'
        self.s9a = '[b'
        self.s10 = 'b['
        self.s10a = '[c'

        self.cirque_strings = [
            "ringling bros circus - orlando - florida",
            "the amazing ringling bros",
            "ringling bros circus orlando",
            "amazing circus orlando",
            "florida ringling bros at the amway center",
            "circus - ringling bros - amway center"
        ]

        self.baseball_strings = [
            "san francisco giants vs oakland athletics",
            "oakland athletics vs los angeles angels",
            "baltimore orioles vs los angeles dodgers",
            "dodgers vs giants",
        ]

    def tearDown(self):
        pass

    def testEqual_public(self):
        self.assertEqual(fuzz.ratio(self.s1, self.s1a), 100)
        self.assertEqual(fuzz.ratio(self.s8, self.s8a), 100)
        self.assertEqual(fuzz.ratio(self.s9, self.s9a), 100)

    def testCaseInsensitive_public(self):
        self.assertNotEqual(fuzz.ratio(self.s1, self.s2), 100)
        self.assertEqual(fuzz.ratio(utils.full_process(self.s1), utils.full_process(self.s2)), 100)

    def testPartialRatio_public(self):
        self.assertEqual(fuzz.partial_ratio(self.s1, self.s3), 100)

    def testTokenSortRatio_public(self):
        self.assertEqual(fuzz.token_sort_ratio(self.s1, self.s1a), 100)

    def testPartialTokenSortRatio_public(self):
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s1, self.s1a), 100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s4, self.s5), 100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s8, self.s8a, full_process=False), 100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s9, self.s9a, full_process=True), 100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s9, self.s9a, full_process=False), 100)
        self.assertEqual(fuzz.partial_token_sort_ratio(self.s10, self.s10a, full_process=False), 50)

    def testTokenSetRatio_public(self):
        self.assertEqual(fuzz.token_set_ratio(self.s4, self.s5), 100)
        self.assertEqual(fuzz.token_set_ratio(self.s8, self.s8a, full_process=False), 100)
        self.assertEqual(fuzz.token_set_ratio(self.s9, self.s9a, full_process=True), 100)
        self.assertEqual(fuzz.token_set_ratio(self.s9, self.s9a, full_process=False), 100)
        self.assertEqual(fuzz.token_set_ratio(self.s10, self.s10a, full_process=False), 50)

    def testPartialTokenSetRatio_public(self):
        self.assertEqual(fuzz.partial_token_set_ratio(self.s4, self.s7), 100)

    def testQuickRatioEqual_public(self):
        self.assertEqual(fuzz.QRatio(self.s1, self.s1a), 100)

    def testQuickRatioCaseInsensitive_public(self):
        self.assertEqual(fuzz.QRatio(self.s1, self.s2), 100)

    def testQuickRatioNotEqual_public(self):
        self.assertNotEqual(fuzz.QRatio(self.s1, self.s3), 100)

    def testWRatioEqual_public(self):
        self.assertEqual(fuzz.WRatio(self.s1, self.s1a), 100)

    def testWRatioCaseInsensitive_public(self):
        self.assertEqual(fuzz.WRatio(self.s1, self.s2), 100)

    def testWRatioNotEqual_public(self):
        self.assertNotEqual(fuzz.WRatio(self.s1, self.s3), 100)


# Remaining derived tests could be written similarly for coverage, focusing on changed values