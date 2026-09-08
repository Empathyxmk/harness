"""Public test for latexify.frontend with different function."""

import math
from src.latexify import frontend

def test_latexify_expression_public():
    def func(a, b):
        return a**3 + b**3

    latex = frontend.latexify(func)  # Should generate a latex string for this function
    assert r"(a^{3} + b^{3})" in latex or r"a^{3}" in latex  # Loosely check structure

def test_latexify_with_config_public():
    def mulsub(x, y):
        temp = x * y
        return temp - y

    latex = frontend.latexify(mulsub, reduce_assignments=True)
    # Should contain assignment for temp
    assert "temp" in latex or "\\mathrm{temp}" in latex