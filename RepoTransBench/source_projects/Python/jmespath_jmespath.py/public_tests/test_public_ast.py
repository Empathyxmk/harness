import pytest
import jmespath.ast as ast


def test_comparator():
    c = ast.comparator('ne', {'type': 'literal', 'value': 5, 'children': []}, {'type': 'literal', 'value': 3, 'children': []})
    assert c['type'] == 'comparator'
    assert c['children'][0]['value'] == 5
    assert c['value'] == 'ne'


def test_current_node():
    c = ast.current_node()
    assert c['type'] == 'current'
    assert c['children'] == []


def test_expref():
    e = ast.expref({'type': 'field', 'value': 'abc', 'children': []})
    assert e['type'] == 'expref'
    assert e['children'][0]['type'] == 'field'


def test_function_expression():
    fe = ast.function_expression('bar', [{'type': 'literal', 'value': 10, 'children': []}])
    assert fe['type'] == 'function_expression'
    assert fe['value'] == 'bar'
    assert fe['children'][0]['value'] == 10


def test_field():
    f = ast.field('bar')
    assert f['type'] == 'field'
    assert f['value'] == 'bar'


def test_filter_projection():
    fp = ast.filter_projection({'type': 'field', 'value': 'id', 'children': []}, {'type': 'foo', 'children': []}, {'type': 'baz', 'children': []})
    assert fp['type'] == 'filter_projection'
    assert len(fp['children']) == 3


def test_flatten():
    node = {'type': 'field', 'value': 'x', 'children': []}
    flat = ast.flatten(node)
    assert flat['type'] == 'flatten'
    assert flat['children'][0] == node


def test_identity():
    node = ast.identity()
    assert node['type'] == 'identity'
    assert node['children'] == []


def test_index():
    node = ast.index(7)
    assert node['type'] == 'index'
    assert node['value'] == 7


def test_index_expression():
    node = ast.index_expression([ast.literal('b')])
    assert node['type'] == 'index_expression'
    assert node['children'][0]['value'] == 'b'


def test_key_val_pair():
    node = ast.key_val_pair('z', ast.literal(7))
    assert node['type'] == 'key_val_pair'
    assert node['value'] == 'z'
    assert node['children'][0]['value'] == 7


def test_literal():
    l = ast.literal({'baz': 'qux'})
    assert l['type'] == 'literal'
    assert l['value'] == {'baz': 'qux'}


def test_multi_select_dict():
    nodes = [ast.literal(4)]
    m = ast.multi_select_dict(nodes)
    assert m['type'] == 'multi_select_dict'
    assert m['children'] == nodes


def test_multi_select_list():
    nodes = [ast.literal(6)]
    m = ast.multi_select_list(nodes)
    assert m['type'] == 'multi_select_list'
    assert m['children'] == nodes


def test_or_expression():
    a = ast.literal(10)
    b = ast.literal(20)
    node = ast.or_expression(a, b)
    assert node['type'] == 'or_expression'
    assert node['children'][0]['value'] == 10


def test_and_expression():
    a = ast.literal(3)
    b = ast.literal(4)
    node = ast.and_expression(a, b)
    assert node['type'] == 'and_expression'
    assert node['children'][1]['value'] == 4


def test_not_expression():
    a = ast.literal(True)
    node = ast.not_expression(a)
    assert node['type'] == 'not_expression'
    assert node['children'][0]['value'] is True


def test_pipe():
    l = ast.literal(12)
    r = ast.literal(24)
    p = ast.pipe(l, r)
    assert p['type'] == 'pipe'
    assert p['children'][1]['value'] == 24


def test_projection():
    l = ast.literal(13)
    r = ast.literal(14)
    p = ast.projection(l, r)
    assert p['type'] == 'projection'
    assert p['children'][0]['value'] == 13
    assert p['children'][1]['value'] == 14


def test_subexpression():
    children = [ast.literal(6), ast.literal(16)]
    s = ast.subexpression(children)
    assert s['type'] == 'subexpression'
    assert s['children'][1]['value'] == 16


def test_slice():
    node = ast.slice(2, 6, 1)
    assert node['type'] == 'slice'
    assert len(node['children']) == 3


def test_value_projection():
    l = ast.literal(7)
    r = ast.literal(8)
    node = ast.value_projection(l, r)
    assert node['type'] == 'value_projection'
    assert node['children'][1]['value'] == 8