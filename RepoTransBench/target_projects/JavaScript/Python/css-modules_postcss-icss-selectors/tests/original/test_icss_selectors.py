import pytest

from src.icss_selectors import rewrite_selectors_with_icss

def normalize_css(css: str) -> str:
    """Collapse all whitespace to single spaces for comparison, like JS tests."""
    import re
    return re.sub(r"\s+", " ", css).strip()

class TestIcssSelectorsOriginal:
    def test_rewrite_selectors_with_icss_selector(self):
        input_css = """
          :icss-selector {
            -icss-selector: .myClass;
          }
          .myClass {
            color: red;
          }
        """
        expected = """
          .myClass {
            color: red;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)

    def test_rewrite_multiple_selectors(self):
        input_css = """
          :icss-selector {
            -icss-selector: .a;
          }
          .a .b {
            background: white;
          }
          :icss-selector {
            -icss-selector: #main;
          }
          #main .header {
            color: green;
          }
        """
        # All rules start with the last selector (#main)
        expected = """
          #main .b {
            background: white;
          }
          #main .header {
            color: green;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)

    def test_removes_icss_selector_block(self):
        input_css = """
          :icss-selector {
            -icss-selector: .alpha;
          }
          .alpha {
            font-size: 16px;
          }
          .beta {
            font-size: 12px;
          }
        """
        # All rules start with .alpha due to rewrite
        expected = """
          .alpha {
            font-size: 16px;
          }
          .alpha {
            font-size: 12px;
          }
        """
        result = rewrite_selectors_with_icss(input_css)
        assert normalize_css(result) == normalize_css(expected)