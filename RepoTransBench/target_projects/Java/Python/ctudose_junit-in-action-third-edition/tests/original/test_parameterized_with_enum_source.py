import pytest

class WordCounter:
    def count_words(self, sentence):
        # Split on whitespace and filter out empty splits
        return len([w for w in sentence.split() if w.strip()])

class Sentences:
    JUNIT_IN_ACTION = "JUnit in Action"
    SOME_PARAMETERS = "Check some parameters"
    THREE_PARAMETERS = "Check three parameters"

    @classmethod
    def all(cls):
        return [
            cls.JUNIT_IN_ACTION,
            cls.SOME_PARAMETERS,
            cls.THREE_PARAMETERS
        ]

@pytest.mark.parametrize("sentence", Sentences.all())
def test_words_in_sentence(sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == 3

@pytest.mark.parametrize("sentence", [Sentences.JUNIT_IN_ACTION, Sentences.THREE_PARAMETERS])
def test_selected_words_in_sentence(sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == 3

@pytest.mark.parametrize("sentence", [Sentences.JUNIT_IN_ACTION, Sentences.SOME_PARAMETERS])
def test_excluded_words_in_sentence(sentence):
    word_counter = WordCounter()
    assert word_counter.count_words(sentence) == 3