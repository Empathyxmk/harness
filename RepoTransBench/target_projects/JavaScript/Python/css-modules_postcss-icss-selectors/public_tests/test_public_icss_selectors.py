import pytest

from src.icss_selectors import rewrite_selectors_with_icss

def normalize_css(css: str) -> str:
    """Collapse all whitespace to single spaces for comparison."""
    import re
    return re.sub(r"\s+", " ", css).strip()

class TestIcssSelectorsPublic:
    def test_rewrite_selectors_with_icss_selector_public(self):
        input_css = """
          :icss-selector {
            -icss-selector: .publicClass;
          }
          .publicClass {
            color: blue;
          }
        """
        expected = """
          .publicClass {
            color: blue;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)

    def test_rewrite_multiple_selectors_public(self):
        input_css = """
          :icss-selector {
            -icss-selector: .x;
          }
          .x .y {
            background: yellow;
          }
          :icss-selector {
            -icss-selector: #different;
          }
          #different .footer {
            color: pink;
          }
        """
        # All rules should begin with the last selector: #different
        expected = """
          #different .y {
            background: yellow;
          }
          #different .footer {
            color: pink;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)

    def test_removes_icss_selector_block_public(self):
        input_css = """
          :icss-selector {
            -icss-selector: .gamma;
          }
          .gamma {
            font-weight: bold;
          }
          .delta {
            font-style: italic;
          }
        """
        # All rules begin with .gamma due to plugin logic
        expected = """
          .gamma {
            font-weight: bold;
          }
          .gamma {
            font-style: italic;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)