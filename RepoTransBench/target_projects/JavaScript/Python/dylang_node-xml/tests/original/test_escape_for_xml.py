import pytest
from xml_module.escape_for_xml import escape_for_xml

class TestEscapeForXML:
    def test_escapes_all_relevant_xml_characters(self):
        assert escape_for_xml('&"\'<>') == '&amp;&quot;&apos;&lt;&gt;'

    def test_returns_input_when_no_escaping_needed(self):
        assert escape_for_xml('abc') == 'abc'

    def test_returns_non_string_input_unchanged(self):
        assert escape_for_xml(5) == 5
        assert escape_for_xml(None) is None

    def test_works_with_empty_string(self):
        assert escape_for_xml('') == ''