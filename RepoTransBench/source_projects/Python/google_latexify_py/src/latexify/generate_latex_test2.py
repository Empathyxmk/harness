import types
import pytest
from latexify import generate_latex
from latexify.exceptions import LatexifyError
from latexify import config as cfg

def simple_fn(x): return x + 1

def fn_with_doc(x): "Docstr"; return x**2

def test_get_latex_function_and_algorithmic(monkeypatch):
    r = generate_latex.get_latex(simple_fn)
    assert isinstance(r, str)
    r2 = generate_latex.get_latex(simple_fn, style=generate_latex.Style.ALGORITHMIC)
    assert isinstance(r2, str)
    r3 = generate_latex.get_latex(simple_fn, style=generate_latex.Style.IPYTHON_ALGORITHMIC)
    assert isinstance(r3, str)

def test_get_latex_merge_config_and_kwargs():
    c = cfg.Config.defaults().merge(use_math_symbols=True)
    out = generate_latex.get_latex(simple_fn, config=c, use_signature=False)
    assert isinstance(out, str)

def test_get_latex_with_transformers(monkeypatch):
    # Patch out transformers so we can force edge cases
    class Dummy:
        def visit(self, tree): return tree
    monkeypatch.setattr(generate_latex, "parser", types.SimpleNamespace(parse_function=lambda f: "tree"))
    monkeypatch.setattr(generate_latex.transformers, "AugAssignReplacer", lambda: Dummy())
    monkeypatch.setattr(generate_latex.transformers, "PrefixTrimmer", lambda p: Dummy())
    monkeypatch.setattr(generate_latex.transformers, "IdentifierReplacer", lambda _d: Dummy())
    monkeypatch.setattr(generate_latex.transformers, "DocstringRemover", lambda: Dummy())
    monkeypatch.setattr(generate_latex.transformers, "AssignmentReducer", lambda: Dummy())
    monkeypatch.setattr(generate_latex.transformers, "FunctionExpander", lambda f: Dummy())

    class Codegen:
        def __init__(self, **kwargs): pass
        def visit(self, tree): return "LATEX!"
    monkeypatch.setattr(generate_latex.codegen, "AlgorithmicCodegen", lambda **kw: Codegen())
    monkeypatch.setattr(generate_latex.codegen, "FunctionCodegen", lambda **kw: Codegen())
    monkeypatch.setattr(generate_latex.codegen, "IPythonAlgorithmicCodegen", lambda **kw: Codegen())
    assert generate_latex.get_latex(simple_fn, style=generate_latex.Style.FUNCTION) == "LATEX!"
    assert generate_latex.get_latex(simple_fn, style=generate_latex.Style.ALGORITHMIC) == "LATEX!"
    assert generate_latex.get_latex(simple_fn, style=generate_latex.Style.IPYTHON_ALGORITHMIC) == "LATEX!"

def test_get_latex_unrecognized_style():
    with pytest.raises(ValueError):
        generate_latex.get_latex(simple_fn, style="invalid-style")  # type: ignore