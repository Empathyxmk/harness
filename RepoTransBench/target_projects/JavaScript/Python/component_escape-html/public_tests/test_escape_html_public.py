import pytest
from src.escape_html import escape_html

class TestEscapeHtmlPublic:
    def test_no_escapable_characters(self):
        assert escape_html('Public abc123 test') == 'Public abc123 test'

    def test_escape_double_quote(self):
        assert escape_html('She said: "Hello!"') == 'She said: &quot;Hello!&quot;'

    def test_escape_single_quote(self):
        assert escape_html("It's a public test") == "It&#39;s a public test"

    def test_escape_ampersand(self):
        assert escape_html('Fish & Chips') == 'Fish &amp; Chips'

    def test_escape_less_than_sign(self):
        assert escape_html('<section>') == '&lt;section&gt;'

    def test_multiple_types_of_escapable_characters(self):
        s = '5 > 2 && 2 < 4 "quoted" \'single\''
        expected = '5 &gt; 2 &amp;&amp; 2 &lt; 4 &quot;quoted&quot; &#39;single&#39;'
        assert escape_html(s) == expected

    def test_escape_already_escaped(self):
        s = '&quot; &gt; &#39;'
        expected = '&amp;quot; &amp;gt; &amp;#39;'
        assert escape_html(s) == expected

    def test_number_input(self):
        # Should work with int input
        assert escape_html(2024) == '2024'

    def test_empty_string(self):
        assert escape_html('') == ''

    def test_no_escape_for_unrelated_characters(self):
        # Only escapable characters should be replaced
        s = '!@$%^()[]=+'
        assert escape_html(s) == s