import pytest

class EmojiConverter:
    @classmethod
    def get_instance(cls):
        # Stub for singleton pattern
        # In real code, would use actual implementation
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def to_alias(self, s):
        if s is None:
            raise TypeError("NullPointerException")
        return s  # Demo stub

    def to_unicode(self, s):
        if s is None:
            raise TypeError("NullPointerException")
        return s  # Demo stub

@pytest.fixture
def converter():
    return EmojiConverter.get_instance()

def test_null_input_to_alias(converter):
    with pytest.raises(TypeError):
        converter.to_alias(None)

def test_null_input_to_unicode(converter):
    with pytest.raises(TypeError):
        converter.to_unicode(None)

def test_empty_string(converter):
    assert converter.to_alias("") == ""
    assert converter.to_unicode("") == ""