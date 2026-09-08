import pytest

class TwigLanguage:
    def getDisplayName(self):
        return "Twig"
    def getPreferredExtension(self):
        return "twig"
    def isIdentifierChar(self, c):
        return c.isalpha()
    def getCompletionHandler(self):
        return object()
    def getFormatter(self):
        return object()
    def hasStructureScanner(self):
        return True
    def hasHintsProvider(self):
        return False
    def getStructureScanner(self):
        return object()
    def isUsingCustomEditorKit(self):
        return True
    def hasFormatter(self):
        return True

def test_display_name():
    lang = TwigLanguage()
    assert lang.getDisplayName() == "Twig"
    assert lang.getPreferredExtension() == "twig"

def test_is_identifier_char():
    lang = TwigLanguage()
    assert lang.isIdentifierChar('a')
    assert not lang.isIdentifierChar('1')
    assert not lang.isIdentifierChar('*')

def test_get_completion_handler_and_formatter():
    lang = TwigLanguage()
    cch = lang.getCompletionHandler()
    assert cch is not None
    formatter = lang.getFormatter()
    assert formatter is not None

def test_has_structure_scanner_and_hints_provider():
    lang = TwigLanguage()
    assert lang.hasStructureScanner()
    assert not lang.hasHintsProvider()
    ss = lang.getStructureScanner()
    assert ss is not None

def test_is_using_custom_editor_kit_and_has_formatter():
    lang = TwigLanguage()
    assert lang.isUsingCustomEditorKit()
    assert lang.hasFormatter()