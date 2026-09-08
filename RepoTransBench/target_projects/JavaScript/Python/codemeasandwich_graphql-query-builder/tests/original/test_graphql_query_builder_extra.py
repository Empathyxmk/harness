import pytest

from src.graphql_query_builder.index import Query

def test_should_throw_if_find_called_with_falsy_value():
    q = Query('something')
    with pytest.raises(Exception):
        q.find()
    with pytest.raises(Exception):
        q.find(None)

def test_should_not_throw_if_query_constructed_with_undefined_and_second_arg_present():
    try:
        Query(None, {})
    except Exception:
        pytest.fail("Should NOT throw if Query() constructed with None and dict as second argument.")

def test_should_throw_if_query_constructed_with_invalid_second_argument_type():
    with pytest.raises(Exception):
        Query('test', 5)

def test_should_throw_if_to_string_called_before_find():
    q = Query('test')
    with pytest.raises(Exception):
        str(q)

def test_should_throw_if_parceFind_gets_unhandled_value_type():
    q = Query('test')
    import types
    class DummySym:
        pass
    # We simulate by passing something odd; let's use a plain object not normally handled
    with pytest.raises(Exception):
        q.find(object())

def test_should_support_set_alias_after_construction():
    q = Query('some')
    q.find({"a": 1})
    q.setAlias('alias')
    assert 'alias' in str(q)

def test_should_not_throw_if_find_object_property_is_function():
    class Callable:
        def __call__(self):
            return 42
    q = Query('funprop')
    try:
        q.find({"prop": lambda: 3})
        q.find({"another": Callable()})
    except Exception:
        pytest.fail("Should not throw if find object property is a function (or callable)")

def test_should_skip_empty_objects_in_filter():
    q = Query('test')
    q.find({"a": {}})
    assert 'test' in str(q)

def test_should_work_with_find_as_array_of_single_key_objects():
    q = Query('multi')
    q.find([{"foo": 1}, {"bar": 2}])
    s = str(q)
    assert 'foo' in s
    assert 'bar' in s