class Emoji4Unicode:
    def __init__(self):
        self.categories = None

    def __str__(self):
        return "Emoji4Unicode()"

def test_to_string_and_class_loads():
    emoji = Emoji4Unicode()
    assert str(emoji) is not None
    assert Emoji4Unicode is not None