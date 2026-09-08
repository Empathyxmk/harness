import os
import csv
import pytest

# Place the CSV in data/word_counter.csv in this repo (relative path)
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
CSV_FILE = os.path.abspath(os.path.join(DATA_DIR, "word_counter.csv"))

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize("expected,sentence", [
    (
        int(row["expected"]), row["sentence"]
    )
    for row in csv.DictReader(open(CSV_FILE, newline=''))  # expects column headers: expected,sentence
])
def test_words_in_sentence(expected, sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == expected