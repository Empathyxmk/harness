import pytest

class Language:
    pass

class TwigTopTokenId:
    @staticmethod
    def language():
        return Language()

def test_language_not_null():
    lang = TwigTopTokenId.language()
    assert lang is not None