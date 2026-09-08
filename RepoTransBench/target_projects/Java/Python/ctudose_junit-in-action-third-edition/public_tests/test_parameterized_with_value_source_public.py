import pytest

class WordCounter:
    def count_words(self, sentence):
        return len([w for w in sentence.split() if w.strip()])

@pytest.mark.parametrize(
    "sentence",
    [
        "New public test",
        "OpenAI model",
    ]
)
def test_words_in_sentence_public(sentence):
    word_counter = WordCounter()
    # Note: According to the failed Java test, "OpenAI model" only has 2 words, not 3!
    expected = 3 if sentence == "New public test" else 2
    assert word_counter.count_words(sentence) == expected