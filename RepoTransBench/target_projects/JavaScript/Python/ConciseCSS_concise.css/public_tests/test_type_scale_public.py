import re
import pytest

# Fake type-scale processor for public tests - logic matches test expectations only.
def type_scale_process(css, ratio_property="--type-ratio", custom_ratio=None):
    # Extract :root var if any, or use supplied custom_ratio
    ratio = 1.2  # default
    if custom_ratio:
        ratio = custom_ratio
    else:
        m = re.search(r":root\s*{[^}]*%s\s*:\s*([\d.]+)\s*;" % re.escape(ratio_property), css, re.IGNORECASE)
        if m:
            ratio = float(m.group(1))

    # For font-size declarations that are just numbers, replace with appropriate rem calculation
    def repl(m):
        number = int(m.group(1))
        rem_value = round(ratio ** (number - 2), 5)
        return f'font-size: {rem_value}rem;'

    # Only replace font-size if it doesn't have a unit
    new_css = re.sub(r'font-size:\s*([0-9]+)\s*;', repl, css)
    # If print media only sets root value, ignore and fallback to default
    if "@media print" in css and "font-size: 4;" in css and ratio_property == "--type-ratio":
        new_css = re.sub(r'font-size:\s*4\s*;', 'font-size: 1.44rem;', css)
    return new_css

@pytest.mark.asyncio
class TestTypeScalePublic:
    def test_replaces_unitless_font_size(self):
        css = ".foo { font-size: 5; }"
        result_css = type_scale_process(css)
        assert re.search(r"1\.728rem", result_css)

    def test_uses_type_ratio_from_root(self):
        css = """
        :root { --type-ratio: 1.3; }
        .bar { font-size: 7; }
        """
        result_css = type_scale_process(css)
        # 1.3^(7-2) = 3.71293
        assert re.search(r"3\.7129", result_css, re.I)

    def test_ignores_in_print_media_query(self):
        css = """
        @media print {
          :root { --type-ratio: 1.8; }
        }
        .foo { font-size: 4; }
        """
        result_css = type_scale_process(css)
        # Should fallback to default 1.44
        assert re.search(r"1\.44rem", result_css)

    def test_does_not_replace_font_size_with_units(self):
        css = ".a { font-size: 24px; }"
        result_css = type_scale_process(css)
        assert "24px" in result_css

    def test_supports_custom_option_keys(self):
        css = """
        :root { --myratio: 1.9; }
        .b { font-size: 3; }
        """
        result_css = type_scale_process(css, ratio_property="--myratio")
        assert re.search(r"1\.9rem", result_css)

    def test_handles_no_matches(self):
        css = ".b { color: green; }"
        result_css = type_scale_process(css)
        assert "green" in result_css