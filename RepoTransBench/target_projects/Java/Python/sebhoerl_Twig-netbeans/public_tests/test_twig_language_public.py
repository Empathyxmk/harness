import pytest

class TwigLanguage:
    MIME_TYPE = "text/x-twig"
    _instance = None
    @staticmethod
    def getInstance():
        if TwigLanguage._instance is None:
            TwigLanguage._instance = TwigLanguage()
        return TwigLanguage._instance

def test_get_mime_type_is_not_html():
    assert TwigLanguage.MIME_TYPE != "text/html"

def test_get_instance_is_identical():
    lang_a = TwigLanguage.getInstance()
    lang_b = TwigLanguage.getInstance()
    assert lang_a is lang_b