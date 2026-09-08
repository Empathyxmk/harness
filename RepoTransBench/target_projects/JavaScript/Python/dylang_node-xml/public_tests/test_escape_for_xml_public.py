import pytest
from xml_module.escape_for_xml import escape_for_xml

class TestEscapeForXMLPublic:
    def test_escapes_various_xml_characters(self):
        assert escape_for_xml('<>&\'"') == '&lt;&gt;&amp;&apos;&quot;'

    def test_returns_input_when_no_escaping_needed(self):
        assert escape_for_xml('xyz') == 'xyz'

    def test_returns_non_string_input_unchanged(self):
        assert escape_for_xml(True) is True
        assert escape_for_xml(0) == 0
        assert escape_for_xml(None) is None

    def test_works_with_empty_string(self):
        assert escape_for_xml('') == ''