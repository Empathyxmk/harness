class Emoji4Unicode:
    def __init__(self):
        self._categories = None

    def set_categories(self, categories):
        self._categories = categories

    def get_categories(self):
        return self._categories

def test_emoji4unicode_public_setters_and_getters():
    unicode_ = Emoji4Unicode()
    unicode_.set_categories(None)
    assert unicode_.get_categories() is None