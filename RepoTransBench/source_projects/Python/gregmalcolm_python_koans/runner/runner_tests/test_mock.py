import pytest

import sys
import types
sys.path.insert(0, './libs')
import mock

def test_sentinel_object_repr():
    s = mock.SentinelObject("MY_MARK")
    assert repr(s) == '<SentinelObject "MY_MARK">'

def test_sentinel_attribute_uniqueness():
    s = mock.Sentinel()
    a = s.foo
    b = s.foo
    c = s.bar
    assert a is b
    assert a is not c

def test_default_and_class_type():
    # Check default/sentinel type is same as above
    assert hasattr(mock.sentinel, "DEFAULT")
    assert isinstance(mock.ClassType, type)

def test_dot_lookup_basic():
    # Simulate the _dot_lookup private function
    class X:
        foo = 123
    result = mock._dot_lookup(X, "foo")
    assert result == 123

def test__copy_lists_dicts_tuples_sets():
    # deepcopy operations
    lst = [1,2]
    assert mock._copy(lst) == [1,2]
    dct = {'a':1}
    assert mock._copy(dct) == {'a':1}
    tpl = (1,2)
    assert mock._copy(tpl) == (1,2)
    st = set((1,2))
    assert mock._copy(st) == set([1,2])
    s = 12
    assert mock._copy(s) == 12

def test_mock_basics_and_methods():
    m = mock.Mock()
    m(1,2, x=3)
    assert m.called
    assert m.call_count == 1
    assert m.call_args == ((1,2), {'x':3})
    m.reset_mock()
    assert not m.called
    # with return_value
    m2 = mock.Mock(return_value="abc")
    rv = m2()
    assert rv == "abc"
    # test assert_called_with pass
    m2(1,2)
    m2.assert_called_with(1,2)

def test_mock_side_effect_lambda():
    m = mock.Mock(side_effect=lambda a: a*2)
    assert m(4) == 8

def test_mock_side_effect_exception():
    with pytest.raises(Exception):
        m = mock.Mock(side_effect=Exception("fail"))
        m()

def test_mock_spec_blocks_nonexistent():
    m = mock.Mock(spec=['foo'])
    m.foo
    with pytest.raises(AttributeError):
        m.bar

def test_mock_wraps():
    def f(x): return x+1
    m = mock.Mock(wraps=f)
    assert m(3) == 4

def test_magic_methods_blocked():
    m = mock.Mock()
    with pytest.raises(AttributeError):
        _ = m.__foobar__