import pytest
from src.graphql_query_builder.index import Query

def remove_spaces(s):
    return str(s).replace(' ', '').replace('\t', '').replace('\n', '')

def test_should_accept_single_find_value_public():
    expected = "product{price}"
    q = Query("product").find("price")
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_create_query_with_function_name_and_alias_public():
    expected = "best : product{title}"
    q = Query("product", "best").find("title")
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_create_query_with_function_name_and_input_public():
    expected = "order(orderId:56789){status}"
    q = Query("order", {"orderId": 56789}).find("status")
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_create_query_with_function_name_and_inputs_public():
    expected = "order(orderId:56789, quantity:10){status}"
    q = Query("order", {"orderId": 56789, "quantity": 10}).find("status")
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_accept_array_as_find_argument_public():
    expected = "shop{location, items}"
    q = Query("shop").find(["location", "items"])
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_handle_nested_find_public():
    expected = "profile{id, data{email}}"
    q = Query("profile").find(["id", {"data": ["email"]}])
    assert remove_spaces(expected) == remove_spaces(q)

def test_should_stringify_to_string_correctly_public():
    expected = "team{members}"
    q = Query("team").find("members")
    assert remove_spaces(expected) == remove_spaces(q.to_string())

def test_should_support_to_string_with_simple_case_public():
    expected = "item{name}"
    q = Query("item").find("name")
    assert remove_spaces(expected) == remove_spaces(q.to_string())