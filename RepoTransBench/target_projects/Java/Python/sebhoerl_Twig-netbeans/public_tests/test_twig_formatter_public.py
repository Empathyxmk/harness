import pytest

class TwigFormatter:
    def format(self, input_str):
        # Simulate: if non-Twig, keep input
        if "twig" not in input_str.lower():
            return input_str
        return input_str.strip() or "processed"

def test_format_keeps_input_when_no_twig():
    formatter = TwigFormatter()
    input_str = "<h2>No Twig public!</h2>"
    assert formatter.format(input_str) == input_str

def test_format_handles_twig_block():
    formatter = TwigFormatter()
    input_str = "{% for item in items %}<li>{{ item }}</li>{% endfor %}"
    formatted = formatter.format(input_str)
    assert formatted is not None
    assert formatted != ""