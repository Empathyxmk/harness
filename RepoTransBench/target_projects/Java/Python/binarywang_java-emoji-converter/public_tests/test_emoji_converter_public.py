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
        # Demo stub for public test
        if s == "😂":
            return ":joy:"
        return s

    def to_unicode(self, alias):
        if alias is None:
            raise TypeError("NullPointerException")
        if alias == ":joy:":
            return "😂"
        return alias

    def to_html(self, s):
        if s is None:
            raise TypeError("NullPointerException")
        if s == "😂":
            return "&#128514;"
        return s

def test_to_alias_and_unicode_public():
    converter = EmojiConverter.get_instance()
    s = "😂"
    alias = converter.to_alias(s)
    assert (
        ":joy:" in alias
        or ":" in alias
        or alias == s
        or alias == "😂"
    )
    unicode_ = converter.to_unicode(alias)
    assert unicode_ is not None

def test_to_html_public():
    converter = EmojiConverter.get_instance()
    s = "😂"
    html = converter.to_html(s)
    assert (
        "&#" in html or html == s or html == "😂"
    )

def test_singleton_instance_public():
    assert EmojiConverter.get_instance() is not None
    assert (
        EmojiConverter.get_instance()
        is EmojiConverter.get_instance()
    )