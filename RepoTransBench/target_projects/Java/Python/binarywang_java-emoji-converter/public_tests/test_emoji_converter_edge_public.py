import pytest

class EmojiConverter:
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def to_alias(self, s):
        if s is None:
            raise TypeError("NullPointerException")
        return s

    def to_unicode(self, s):
        if s is None:
            raise TypeError("NullPointerException")
        return s

@pytest.fixture
def converter():
    return EmojiConverter.get_instance()

def test_null_input_to_alias_public(converter):
    with pytest.raises(TypeError):
        converter.to_alias(None)

def test_null_input_to_unicode_public(converter):
    with pytest.raises(TypeError):
        converter.to_unicode(None)

def test_whitespace_string(converter):
    assert converter.to_alias(" ") == " "
    assert converter.to_unicode(" ") == " "