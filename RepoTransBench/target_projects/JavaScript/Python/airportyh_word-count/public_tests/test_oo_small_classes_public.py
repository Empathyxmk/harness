import os
import tempfile
import pytest

# Assumes the classes are in src.oo_small_classes; adjust imports as needed
# from src.oo_small_classes import Tokenizer, FileReader, Tally, Top10Printer, WordCount

# MOCKS: Replace with real ones
class Tokenizer:
    def tokenize(self, s):
        import re
        return [w for w in re.split(r"[\s,\.]+", s) if w != '']

class FileReader:
    def __init__(self, filename):
        self.filename = filename
    def read(self):
        with open(self.filename, encoding='utf-8') as f:
            return f.read()
    def readWords(self):
        return Tokenizer().tokenize(self.read())

class Tally:
    def __init__(self, words):
        from collections import Counter
        self.tally = Counter(words)
        self._words = words
    def getTop10(self):
        top = sorted(
            [{'word': k, 'count': v} for k, v in self.tally.items()],
            key=lambda x: (-x['count'], x['word'])
        )
        return top[:10]

class Top10Printer:
    @staticmethod
    def print(items):
        for entry in items:
            print(f"{entry['word']}: {entry['count']}")

class WordCount:
    @staticmethod
    def main(filename):
        fr = FileReader(filename)
        tally = Tally(fr.readWords())
        Top10Printer.print(tally.getTop10())

def test_tokenizer_splits_correctly_public():
    t = Tokenizer()
    assert t.tokenize('red green,blue') == ['red', 'green', 'blue']

def test_filereader_reads_text_and_words_public(tmp_path):
    WORDS_TEXT = 'dog cat cat, mouse. mouse mouse. rabbit rabbit rabbit rabbit'
    words_file = tmp_path / "test_words2_public.txt"
    words_file.write_text(WORDS_TEXT, encoding='utf-8')
    fr = FileReader(str(words_file))
    assert fr.read() == WORDS_TEXT
    words = fr.readWords()
    assert 'mouse' in words

def test_tally_tallies_sorts_slices_correctly_public(tmp_path):
    WORDS_TEXT = 'dog cat cat, mouse. mouse mouse. rabbit rabbit rabbit rabbit'
    words_file = tmp_path / "test_words2_public.txt"
    words_file.write_text(WORDS_TEXT, encoding='utf-8')
    fr = FileReader(str(words_file))
    tally = Tally(fr.readWords())
    assert tally.tally['mouse'] == 3
    assert tally.tally['rabbit'] == 4
    assert tally.getTop10()[0] == {'word': 'rabbit', 'count': 4}

def test_top10printer_prints_output_public(capsys):
    Top10Printer.print([{'word': 'bar', 'count': 6}])
    captured = capsys.readouterr()
    assert captured.out.strip() != ''

def test_wordcount_main_executes_without_error_public(tmp_path, capsys):
    WORDS_TEXT = 'dog cat cat, mouse. mouse mouse. rabbit rabbit rabbit rabbit'
    words_file = tmp_path / "test_words2_public.txt"
    words_file.write_text(WORDS_TEXT, encoding='utf-8')
    WordCount.main(str(words_file))
    captured = capsys.readouterr()
    assert captured.out.strip() != ''