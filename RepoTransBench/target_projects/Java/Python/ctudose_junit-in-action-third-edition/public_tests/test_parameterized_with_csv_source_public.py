import pytest

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize(
    "expected,sentence",
    [
        (1, "Hello"),
        (5, "This is a public test"),
        (2, "Hello World"),
    ]
)
def test_words_in_sentence_public(expected, sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == expected