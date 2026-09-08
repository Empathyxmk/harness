import pytest
from pybars import Compiler
import src.helpers as helpers

def render_template(tmpl, context):
    compiler = Compiler()
    template = compiler.compile(tmpl)
    return template(context, helpers=helpers.get_helpers())

def test_is_helper_public_boolean_context():
    tmpl = '{{#is active}}PASS{{else}}FAIL{{/is}}'
    context = {'active': False}
    assert render_template(tmpl, context) == 'FAIL'

    context = {'active': True}
    assert render_template(tmpl, context) == 'PASS'

def test_is_helper_public_equality():
    tmpl = '{{#is foo bar}}PASS{{else}}FAIL{{/is}}'
    context = {'foo': 'x', 'bar': 'x'}
    assert render_template(tmpl, context) == 'PASS'

    context = {'foo': 5, 'bar': 6}
    assert render_template(tmpl, context) == 'FAIL'

def test_is_helper_public_operator():
    tmpl = '{{#is score "<" max}}PASS{{else}}FAIL{{/is}}'
    context = {'score': 4, 'max': 10}
    assert render_template(tmpl, context) == 'PASS'

    context = {'score': 10, 'max': 4}
    assert render_template(tmpl, context) == 'FAIL'

def test_is_helper_public_in_operator():
    tmpl = '{{#is foo "in" group}}IN{{else}}OUT{{/is}}'
    context = {'foo': 2, 'group': [1, 2, 3, 4]}
    assert render_template(tmpl, context) == 'IN'

    context = {'foo': 10, 'group': [1, 2, 3, 4]}
    assert render_template(tmpl, context) == 'OUT'

def test_is_helper_public_not_in_operator():
    tmpl = '{{#is foo "not in" group}}NOTIN{{else}}IN{{/is}}'
    context = {'foo': 2, 'group': [1, 2, 3, 4]}
    assert render_template(tmpl, context) == 'IN'

    context = {'foo': 7, 'group': [1, 2, 3, 4]}
    assert render_template(tmpl, context) == 'NOTIN'