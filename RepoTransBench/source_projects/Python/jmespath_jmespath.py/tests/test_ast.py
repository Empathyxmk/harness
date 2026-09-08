import pytest
import jmespath.ast as ast


def test_comparator():
    c = ast.comparator('eq', {'type': 'literal', 'value': 1, 'children': []}, {'type': 'literal', 'value': 2, 'children': []})
    assert c['type'] == 'comparator'
    assert c['children'][0]['value'] == 1
    assert c['value'] == 'eq'


def test_current_node():
    c = ast.current_node()
    assert c['type'] == 'current'
    assert c['children'] == []


def test_expref():
    e = ast.expref({'type': 'identity', 'children': []})
    assert e['type'] == 'expref'
    assert e['children'][0]['type'] == 'identity'


def test_function_expression():
    fe = ast.function_expression('foo', [{'type': 'literal', 'value': 1, 'children': []}])
    assert fe['type'] == 'function_expression'
    assert fe['value'] == 'foo'
    assert fe['children'][0]['value'] == 1


def test_field():
    f = ast.field('foo')
    assert f['type'] == 'field'
    assert f['value'] == 'foo'


def test_filter_projection():
    fp = ast.filter_projection({'type': 'identity', 'children': []}, {'type': 'foo', 'children': []}, {'type': 'bar', 'children': []})
    assert fp['type'] == 'filter_projection'
    assert len(fp['children']) == 3


def test_flatten():
    node = {'type': 'identity', 'children': []}
    flat = ast.flatten(node)
    assert flat['type'] == 'flatten'
    assert flat['children'][0] == node


def test_identity():
    node = ast.identity()
    assert node['type'] == 'identity'
    assert node['children'] == []


def test_index():
    node = ast.index(3)
    assert node['type'] == 'index'
    assert node['value'] == 3


def test_index_expression():
    node = ast.index_expression([ast.literal('a')])
    assert node['type'] == 'index_expression'
    assert node['children'][0]['value'] == 'a'


def test_key_val_pair():
    node = ast.key_val_pair('k', ast.literal(42))
    assert node['type'] == 'key_val_pair'
    assert node['value'] == 'k'
    assert node['children'][0]['value'] == 42


def test_literal():
    l = ast.literal({'foo': 'bar'})
    assert l['type'] == 'literal'
    assert l['value'] == {'foo': 'bar'}


def test_multi_select_dict():
    nodes = [ast.literal(3)]
    m = ast.multi_select_dict(nodes)
    assert m['type'] == 'multi_select_dict'
    assert m['children'] == nodes


def test_multi_select_list():
    nodes = [ast.literal(5)]
    m = ast.multi_select_list(nodes)
    assert m['type'] == 'multi_select_list'
    assert m['children'] == nodes


def test_or_expression():
    a = ast.literal(1)
    b = ast.literal(2)
    node = ast.or_expression(a, b)
    assert node['type'] == 'or_expression'
    assert node['children'][0]['value'] == 1


def test_and_expression():
    a = ast.literal(1)
    b = ast.literal(2)
    node = ast.and_expression(a, b)
    assert node['type'] == 'and_expression'
    assert node['children'][1]['value'] == 2


def test_not_expression():
    a = ast.literal(False)
    node = ast.not_expression(a)
    assert node['type'] == 'not_expression'
    assert node['children'][0]['value'] is False


def test_pipe():
    l = ast.literal(1)
    r = ast.literal(2)
    p = ast.pipe(l, r)
    assert p['type'] == 'pipe'
    assert p['children'][1]['value'] == 2


def test_projection():
    l = ast.literal(1)
    r = ast.literal(2)
    p = ast.projection(l, r)
    assert p['type'] == 'projection'
    assert p['children'][0]['value'] == 1
    assert p['children'][1]['value'] == 2


def test_subexpression():
    children = [ast.literal(1), ast.literal(2)]
    s = ast.subexpression(children)
    assert s['type'] == 'subexpression'
    assert s['children'][1]['value'] == 2


def test_slice():
    node = ast.slice(0, 10, 2)
    assert node['type'] == 'slice'
    assert len(node['children']) == 3


def test_value_projection():
    l = ast.literal(3)
    r = ast.literal(4)
    node = ast.value_projection(l, r)
    assert node['type'] == 'value_projection'
    assert node['children'][1]['value'] == 4