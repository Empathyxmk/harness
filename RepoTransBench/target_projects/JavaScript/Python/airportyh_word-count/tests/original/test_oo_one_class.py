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

def test_should_read_file_content_correctly(tmp_path):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    assert wc.content() == WORDS_TEXT

def test_should_split_words_properly_no_empty_strings(tmp_path):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    assert wc.words() == [
        'Apple', 'apple', 'Banana', 'banana', 'banana', 'Cat', 'cat', 'dog', 'dog', 'dog'
    ]

def test_should_handle_empty_file_gracefully(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text('', encoding="utf-8")
    wc = WordCount(str(empty_file))
    # Emulate JS logic: split returns ['']
    assert wc.words() == ['']
    tally = wc.tally()
    assert '' in tally and tally[''] == 1

def test_should_tally_words_case_insensitively(tmp_path):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    tally = wc.tally()
    assert tally['banana'] == 3
    assert tally['apple'] == 2
    assert tally['cat'] == 2
    assert tally['dog'] == 3

def test_should_return_top_10_entries(tmp_path):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    top = wc.top10()
    assert top[0]['word'] == 'banana'
    assert top[0]['count'] == 3
    top_words = [e['word'] for e in top]
    assert 'dog' in top_words
    assert 'apple' in top_words
    assert 'cat' in top_words

def test_should_handle_ties_in_top10(tmp_path):
    ties_file = tmp_path / "ties.txt"
    ties_file.write_text('one two one two three', encoding="utf-8")
    wc = WordCount(str(ties_file))
    top = wc.top10()
    assert top[0]['count'] == 2
    assert top[1]['count'] == 2

def test_should_printTop10_as_expected(tmp_path, capsys):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    wc = WordCount(str(words_file))
    wc.printTop10()
    captured = capsys.readouterr()
    # Output should not be empty; printTop10 did print
    assert captured.out.strip() != ''

def test_main_should_run_without_throwing(tmp_path, capsys):
    WORDS_TEXT = 'Apple apple Banana banana banana. Cat cat dog, dog dog'
    words_file = tmp_path / "test_words.txt"
    words_file.write_text(WORDS_TEXT, encoding="utf-8")
    WordCount.main(str(words_file))
    captured = capsys.readouterr()
    assert captured.out.strip() != ''

def test_top10_returns_no_more_than_10_results(tmp_path):
    tenplus_file = tmp_path / "tenplus.txt"
    tenplus_file.write_text(' '.join(f'w{i}' for i in range(15)), encoding="utf-8")
    wc = WordCount(str(tenplus_file))
    assert len(wc.top10()) == 10