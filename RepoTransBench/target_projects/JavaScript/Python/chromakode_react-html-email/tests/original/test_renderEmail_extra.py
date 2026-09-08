import pytest
from src.renderEmail import render_email

def test_returns_doctype_and_markup_simple_tree():
    class Comp:
        def __call__(self):
            return "<html><body><h1>Hi!</h1></body></html>"
    output = render_email(Comp())
    assert output.startswith("<!DOCTYPE html")
    assert "<h1>Hi!</h1>" in output

def test_works_with_bare_div():
    class DummyDiv:
        tag = 'div'
    output = render_email(DummyDiv())
    assert "<div" in output