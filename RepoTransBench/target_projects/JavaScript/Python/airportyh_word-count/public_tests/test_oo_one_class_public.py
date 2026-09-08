import os
import tempfile
import pytest

# Assumes the module/class WordCount is in src.oo_one_class, adjust import as needed
# from src.oo_one_class import WordCount

# MOCK IMPLEMENTATION (remove/comment out when real code is available)
class WordCount:
    def __init__(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            self._content = f.read()
        self._words = self._split_words(self._content)
    def content(self):
        return self._content
    def words(self):
        return self._words.copy()
    def tally(self):
        from collections import Counter
        return Counter([(w.lower() if w != '' else '') for w in self._words])
    def top10(self):
        counts = self.tally()
        lst = [{'word': k, 'count': v} for k, v in counts.items()]
        lst.sort(key=lambda x: (-x['count'], x['word']))
        return lst[:10]
    def printTop10(self):
        for entry in self.top10():
            print(f"{entry['word']}: {entry['count']}")
    @staticmethod
    def main(filename):
        wc = WordCount(filename)
        wc.printTop10()
    @staticmethod
    def _split_words(s):
        import re
        # Similar split to JS: split on non-word characters but retain empty when content is empty
        if s == '':
            return ['']
        return [w for w in re.split(r"[\s,.]+", s) if w != '']

def test_should_read_file_content_correctly_public(tmp_path):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    assert wc.content() == WORDS_TEXT

def test_should_split_words_properly_and_avoid_empty_strings_public(tmp_path):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    assert wc.words() == [
        'Red', 'red', 'Blue', 'blue', 'blue', 'Green', 'green', 'yellow', 'yellow', 'yellow'
    ]

def test_should_handle_empty_file_gracefully_public(tmp_path):
    empty_file = tmp_path / "empty_public.txt"
    empty_file.write_text('', encoding="utf-8")
    wc = WordCount(str(empty_file))
    assert wc.words() == ['']
    tally = wc.tally()
    assert '' in tally and tally[''] == 1

def test_should_tally_words_case_insensitively_public(tmp_path):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    tally = wc.tally()
    assert tally['blue'] == 3
    assert tally['red'] == 2
    assert tally['green'] == 2
    assert tally['yellow'] == 3

def test_should_return_top_10_entries_public(tmp_path):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    top = wc.top10()
    assert top[0]['word'] == 'blue'
    assert top[0]['count'] == 3
    top_words = [e['word'] for e in top]
    assert 'red' in top_words
    assert 'green' in top_words
    assert 'yellow' in top_words

def test_should_handle_ties_in_top10_public(tmp_path):
    ties_file = tmp_path / "ties_public.txt"
    ties_file.write_text('alpha beta alpha beta gamma', encoding="utf-8")
    wc = WordCount(str(ties_file))
    top = wc.top10()
    assert top[0]['count'] == 2
    assert top[1]['count'] == 2

def test_should_printTop10_as_expected_public(tmp_path, capsys):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    wc.printTop10()
    captured = capsys.readouterr()
    assert captured.out.strip() != ''

def test_main_should_run_without_throwing_public(tmp_path, capsys):
    WORDS_TEXT = 'Red red Blue blue blue. Green green yellow, yellow yellow'
    words_file = tmp_path / "test_words_public.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    WordCount.main(str(words_file))
    captured = capsys.readouterr()
    assert captured.out.strip() != ''

def test_top10_returns_no_more_than_10_results_public(tmp_path):
    tenplus_file = tmp_path / "tenplus_public.txt"
    tenplus_file.write_text(' '.join(f'p{i}' for i in range(12)), encoding="utf-8")
    wc = WordCount(str(tenplus_file))
    assert len(wc.top10()) == 10