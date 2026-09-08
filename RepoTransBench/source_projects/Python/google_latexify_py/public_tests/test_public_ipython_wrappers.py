"""Public tests for latexify.ipython_wrappers."""

import src.latexify.ipython_wrappers as ipy_wrappers

def test_repr_latex_public():
    class DummyFunc:
        def __init__(self, latex):
            self._latex = latex
        def _latex_(self):
            return self._latex
    dummy = DummyFunc(r"A_{test}")
    result = ipy_wrappers._repr_latex_(dummy)
    assert result == r"A_{test}"


def test_register_latex_for_functions_public(monkeypatch):
    called = []

    def _latex_(self):
        called.append(self)
        return "L"

    class Dummy:
        pass

    orig = getattr(Dummy, "_latex_", None)
    ipy_wrappers.register_latex_for_functions(Dummy)
    d = Dummy()
    # no _latex_ on Dummy; function shoudn't error and should not call anything
    assert hasattr(Dummy, "_latex_")
    # Patch Dummy's _latex_ to our function and check it's called
    Dummy._latex_ = _latex_
    assert d._latex_() == "L"
    assert called == [d]
    # Cleanup
    if orig is not None:
        Dummy._latex_ = orig