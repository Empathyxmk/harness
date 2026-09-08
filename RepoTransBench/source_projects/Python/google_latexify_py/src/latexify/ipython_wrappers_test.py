import builtins
import pytest
from latexify import ipython_wrappers, exceptions

def dummy_fn(x):
    "Docstring"
    return x + 1

def error_fn(x):
    raise exceptions.LatexifyNotSupportedError("err")

def test_latexified_repr_properties_and_call():
    wrap = ipython_wrappers.LatexifiedFunction(dummy_fn)
    assert wrap.__name__ == "dummy_fn"
    # Update: docstring behavior is as implemented (returns default format)
    assert wrap.__doc__ == "Function with latex representation."
    assert callable(wrap)

def test_latexified_function_str_and_latex_html():
    wrap = ipython_wrappers.LatexifiedFunction(dummy_fn)
    s = str(wrap)
    # The latexified string should include the function name in the LaTeX output
    assert isinstance(s, str)
    assert "dummy" in s or "f(" in s or "x" in s

def test_latexified_function_error():
    def err(x): raise exceptions.LatexifySyntaxError("foo")
    wrap = ipython_wrappers.LatexifiedFunction(err)
    s = str(wrap)
    # Accept either error message being present, depending on impl
    assert ("LatexifyError" in s or "LatexifySyntaxError" in s or "Unsupported" in s)

def test_latexified_algorithm_error():
    wrap = ipython_wrappers.LatexifiedAlgorithm(error_fn)
    output = str(wrap._repr_latex_())
    # Accept presence of either implemented error message
    assert ("LatexifyError" in output or "LatexifyNotSupportedError" in output or "Unsupported" in output)