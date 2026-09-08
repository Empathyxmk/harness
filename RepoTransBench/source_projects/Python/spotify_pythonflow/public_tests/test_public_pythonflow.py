import random
import pytest
import pythonflow as pf

def test_consistent_context_public():
    with pf.Graph() as graph:
        uniform = pf.func_op(random.uniform, 2, 3)
        scaled = uniform * 7
    _uniform, _scaled = graph([uniform, scaled])
    assert _scaled == 7 * _uniform

def test_context_public():
    with pf.Graph() as graph:
        a = pf.placeholder(name='a')
        b = pf.placeholder(name='b')
        c = pf.placeholder(name='c')
        x = a * b + c
    actual = graph(x, {a: 2, 'b': 6}, c=4)
    assert actual == 16

def test_iter_public():
    with pf.Graph() as graph:
        pf.constant('xyz', name='letters', length=3)
    x, y, z = graph['letters']
    assert graph([x, y, z]) == tuple('xyz')

def test_getattr_public():
    with pf.Graph() as graph:
        imag = pf.constant(5 + 8j).imag
    assert graph(imag) == 8

class MatmulDummyPublic:
    def __init__(self, value):
        self.value = value
    def __matmul__(self, other):
        if isinstance(other, pf.Operation):
            return NotImplemented
        return self.value * other

@pytest.fixture(params=[
    ('+', 4, 3),
    ('-', 10, 2.0),
    ('*', 5, 12),
    ('@', MatmulDummyPublic(4), 6),
    ('/', 10, 2),
    ('//', 9, 2),
    ('%', 13, 7),
    ('&', 0xab, 0x43),
    ('|', 0x21, 0x88),
    ('^', 0xfe, 0xa2),
    ('**', 3, 4),
    ('<<', 7, 2),
    ('>>', 18, 1),
    ('==', 5, 5),
    ('!=', 5, 9),
    ('>', 9, 7),
    ('>=', 16, 16),
    ('<', 2, 4),
    ('<=', 4, 8),
])
def binary_operators_public(request):
    operator, a, b = request.param
    expected = eval('a %s b' % operator)
    return operator, a, b, expected

def test_binary_operators_left_public(binary_operators_public):
    operator, a, b, expected = binary_operators_public
    with pf.Graph() as graph:
        _a = pf.constant(a)
        operation = eval('_a %s b' % operator)
    actual = graph(operation)
    assert actual == expected

def test_binary_operators_right_public(binary_operators_public):
    operator, a, b, expected = binary_operators_public
    with pf.Graph() as graph:
        _b = pf.constant(b)
        operation = eval('a %s _b' % operator)
    actual = graph(operation)
    assert actual == expected

@pytest.mark.parametrize('operator, value', [
    ('~', 3),
    ('~', 7),
    ('-', 5),
    ('+', 12),
])
def test_unary_operators_public(value, operator):
    expected = eval('%s value' % operator)
    with pf.Graph() as graph:
        operation = eval('%s pf.constant(value)' % operator)
    actual = graph(operation)
    assert actual == expected

def test_contains_public():
    with pf.Graph() as graph:
        test = pf.placeholder()
        letters = pf.constant('xyz')
        contains = pf.contains(letters, test)
    assert graph(contains, {test: 'y'})
    assert not graph(contains, {test: 'a'})

def test_abs_public():
    with pf.Graph() as graph:
        absolute = abs(pf.constant(-123))
    assert graph(absolute) == 123

def test_reversed_public():
    with pf.Graph() as graph:
        rev = reversed(pf.constant('lmn'))
    assert list(graph(rev)) == list('nml')