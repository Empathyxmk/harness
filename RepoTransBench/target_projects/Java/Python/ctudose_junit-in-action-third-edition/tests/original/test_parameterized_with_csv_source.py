import pytest

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize(
    "expected,sentence",
    [
        (2, "Unit testing"),
        (3, "JUnit in Action"),
        (4, "Write solid Java code"),
    ]
)
def test_words_in_sentence(expected, sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == expected