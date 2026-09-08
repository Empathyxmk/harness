import pytest
from pybars import Compiler
import src.helpers as helpers

def render_template(tmpl, context):
    compiler = Compiler()
    template = compiler.compile(tmpl)
    return template(context, helpers=helpers.get_helpers())

def test_is_helper_string_gt():
    tmpl = '{{#is foo ">" bar}}A{{else}}B{{/is}}'
    assert render_template(tmpl, {'foo': 'c', 'bar': 'b'}) == 'A'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'd'}) == 'B'

def test_is_helper_string_gte():
    tmpl = '{{#is foo ">=" bar}}A{{else}}B{{/is}}'
    assert render_template(tmpl, {'foo': 'c', 'bar': 'c'}) == 'A'
    assert render_template(tmpl, {'foo': 'c', 'bar': 'b'}) == 'A'
    assert render_template(tmpl, {'foo': 'b', 'bar': 'c'}) == 'B'

def test_is_helper_string_lt():
    tmpl = '{{#is foo "<" bar}}A{{else}}B{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'b'}) == 'A'
    assert render_template(tmpl, {'foo': 'c', 'bar': 'a'}) == 'B'

def test_is_helper_string_lte():
    tmpl = '{{#is foo "<=" bar}}A{{else}}B{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'a'}) == 'A'
    assert render_template(tmpl, {'foo': 'a', 'bar': 'b'}) == 'A'
    assert render_template(tmpl, {'foo': 'c', 'bar': 'a'}) == 'B'

def test_is_helper_edge_cases():
    # No operator, too many args, or bad operator
    tmpl = '{{#is foo bar baz}}A{{else}}B{{/is}}'
    with pytest.raises(ValueError):
        render_template(tmpl, {'foo': 1, 'bar': 2, 'baz': 3})

    tmpl = '{{#is foo "unknown" bar}}A{{else}}B{{/is}}'
    with pytest.raises(ValueError):
        render_template(tmpl, {'foo': 1, 'bar': 2})

def test_is_helper_bool_conversion():
    tmpl = '{{#is foo}}A{{else}}B{{/is}}'
    assert render_template(tmpl, {'foo': []}) == 'B'
    assert render_template(tmpl, {'foo': [123]}) == 'A'
    assert render_template(tmpl, {'foo': None}) == 'B'
    assert render_template(tmpl, {'foo': 'some-str'}) == 'A'

def test_is_helper_not_in_empty():
    tmpl = '{{#is foo "not in" coll}}X{{else}}Y{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'coll': []}) == 'X'
    assert render_template(tmpl, {'foo': 'a', 'coll': ['a']}) == 'Y'

def test_is_helper_in_empty():
    tmpl = '{{#is foo "in" coll}}X{{else}}Y{{/is}}'
    assert render_template(tmpl, {'foo': 'a', 'coll': []}) == 'Y'
    assert render_template(tmpl, {'foo': 'a', 'coll': ['a']}) == 'X'

def test_is_helper_types_int_str():
    tmpl = '{{#is foo bar}}OK{{else}}NOK{{/is}}'
    assert render_template(tmpl, {'foo': 1, 'bar': '1'}) == 'NOK'
    assert render_template(tmpl, {'foo': '1', 'bar': '1'}) == 'OK'
    assert render_template(tmpl, {'foo': 1, 'bar': 1}) == 'OK'