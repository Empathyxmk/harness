import pytest

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize(
    "sentence",
    [
        "Check three parameters",
        "JUnit in Action",
    ]
)
def test_words_in_sentence(sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == 3