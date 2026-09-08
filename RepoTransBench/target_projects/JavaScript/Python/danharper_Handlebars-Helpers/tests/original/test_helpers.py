import pytest
from pybars import Compiler
import src.helpers as helpers

def render_template(tmpl, context):
    compiler = Compiler()
    template = compiler.compile(tmpl)
    return template(context, helpers=helpers.get_helpers())

def test_is_helper_truthy():
    tmpl = '{{#is a}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'a': True}) == 'PASS'
    assert render_template(tmpl, {'a': 1}) == 'PASS'
    assert render_template(tmpl, {'a': ""}) == 'FAIL'
    assert render_template(tmpl, {'a': 0}) == 'FAIL'

def test_is_helper_equal():
    tmpl = '{{#is foo bar}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'foo': 4, 'bar': 4}) == 'PASS'
    assert render_template(tmpl, {'foo': 4, 'bar': 2}) == 'FAIL'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'a'}) == 'PASS'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'b'}) == 'FAIL'

def test_is_helper_operator_less_than():
    tmpl = '{{#is score "<" max}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'score': 1, 'max': 2}) == 'PASS'
    assert render_template(tmpl, {'score': 4, 'max': 2}) == 'FAIL'

def test_is_helper_operator_greater_than():
    tmpl = '{{#is score ">" max}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'score': 5, 'max': 2}) == 'PASS'
    assert render_template(tmpl, {'score': 1, 'max': 2}) == 'FAIL'

def test_is_helper_operator_in():
    tmpl = '{{#is foo "in" coll}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'coll': ['a', 'b', 'c']}) == 'PASS'
    assert render_template(tmpl, {'foo': 'd', 'coll': ['a', 'b', 'c']}) == 'FAIL'

def test_is_helper_operator_not_in():
    tmpl = '{{#is foo "not in" coll}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'coll': ['a', 'b', 'c']}) == 'FAIL'
    assert render_template(tmpl, {'foo': 'e', 'coll': ['a', 'b', 'c']}) == 'PASS'

def test_is_helper_operator_ne():
    tmpl = '{{#is a "!=" b}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'a': 1, 'b': 1}) == 'FAIL'
    assert render_template(tmpl, {'a': 1, 'b': 2}) == 'PASS'

def test_is_helper_operator_eq():
    tmpl = '{{#is a "==" b}}PASS{{else}}FAIL{{/is}}'
    assert render_template(tmpl, {'a': 1, 'b': 1}) == 'PASS'
    assert render_template(tmpl, {'a': 1, 'b': 2}) == 'FAIL'