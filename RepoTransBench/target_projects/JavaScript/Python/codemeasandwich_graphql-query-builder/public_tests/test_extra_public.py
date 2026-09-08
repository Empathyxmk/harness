import pytest
from src.graphql_query_builder.index import Query

def test_should_throw_if_find_called_with_falsy_value_public():
    q = Query('somethingElse')
    with pytest.raises(Exception):
        q.find(None)
    with pytest.raises(Exception):
        q.find(False)

def test_should_not_throw_if_query_constructed_with_undefined_and_second_arg_is_object():
    try:
        Query(None, {"foo": 42})
    except Exception:
        pytest.fail("Should NOT throw if Query(None, dict) constructed.")

def test_should_throw_if_query_constructed_with_invalid_second_argument_type_public():
    with pytest.raises(Exception):
        Query('sample', True)

def test_should_throw_if_to_string_called_before_find_public():
    q = Query('mytest')
    with pytest.raises(Exception):
        str(q)

def test_should_throw_if_parceFind_gets_unhandled_value_type_public():
    q = Query('bar')
    with pytest.raises(Exception):
        # Simulate BigInt-like unsupported type in JS with a type not normally supported in Python's context
        class DummyBigInt(int):
            pass
        q.find(DummyBigInt(10))

def test_should_support_set_alias_after_construction_public():
    q = Query('jane')
    q.find({"score": 99})
    q.setAlias('otheralias')
    assert 'otheralias' in str(q)