import os
import csv
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CSV_FILE = os.path.abspath(os.path.join(DATA_DIR, "word_counter_public.csv"))

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize("expected,sentence", [
    (
        int(row["expected"]), row["sentence"]
    )
    for row in csv.DictReader(open(CSV_FILE, newline=''))
])
def test_words_in_sentence_public(expected, sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == expected