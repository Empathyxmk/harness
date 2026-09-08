import pytest
from src.code_tag import any, html, css, gql, graphql, md, markdown, sql

def test_returns_raw0_when_no_keys_are_provided_public():
    assert any(["Public test"]) == "Public test"

def test_returns_interpolated_string_when_keys_are_provided_public():
    age = 25
    assert any(["I am ", " years old."], age) == "I am 25 years old."

def test_html_alias_works_the_same_as_any_public():
    assert html(["<span>", "</span>"], 5 * 3) == "<span>15</span>"

def test_css_alias_works_with_template_literals_public():
    assert css([".container { width: ", "; }"], "100%") == ".container { width: 100%; }"

def test_gql_alias_works_public():
    assert gql(["mutation { addUser(name: \"Alice\") }"]) == "mutation { addUser(name: \"Alice\") }"

def test_graphql_alias_works_public():
    assert graphql(["query getUser { name }"]) == "query getUser { name }"

def test_md_alias_works_public():
    assert md(["## Subheader"]) == "## Subheader"

def test_markdown_alias_works_public():
    assert markdown(["1. First item"]) == "1. First item"

def test_sql_alias_works_public():
    assert sql(["UPDATE users SET name='Bob' WHERE id=", ""], 42) == "UPDATE users SET name='Bob' WHERE id=42"

def test_empty_template_returns_empty_string_public():
    assert any([""]) == ""

def test_multiple_interpolations_public():
    x, y, z = "X", "Y", "Z"
    assert any(["", ",", ",", ""], x, y, z) == "X,Y,Z"