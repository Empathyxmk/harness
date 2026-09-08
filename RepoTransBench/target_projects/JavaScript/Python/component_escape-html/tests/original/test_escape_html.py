import pytest
from src.escape_html import escape_html

class TestEscapeHtmlOriginal:
    def test_no_escapable_characters(self):
        assert escape_html('foo bar baz') == 'foo bar baz'

    def test_escape_double_quotes(self):
        assert escape_html('he said "hi"') == 'he said &quot;hi&quot;'

    def test_escape_single_quotes(self):
        assert escape_html("it's ok") == 'it&#39;s ok'

    def test_escape_ampersands(self):
        assert escape_html('AT&T') == 'AT&amp;T'

    def test_escape_less_than(self):
        assert escape_html('1 < 2') == '1 &lt; 2'

    def test_escape_greater_than(self):
        assert escape_html('2 > 1') == '2 &gt; 1'

    def test_multiple_escapable_characters(self):
        s = 'rock & roll > pop < classical "music" ain\'t bad'
        expected = 'rock &amp; roll &gt; pop &lt; classical &quot;music&quot; ain&#39;t bad'
        assert escape_html(s) == expected

    def test_no_double_escape(self):
        # The original logic escapes & first, then the rest
        # E.g., "&quot;" => "&amp;quot;"
        assert escape_html('&quot;') == '&amp;quot;'

    def test_numeric_string(self):
        assert escape_html('12345') == '12345'

    def test_empty_string(self):
        assert escape_html('') == ''