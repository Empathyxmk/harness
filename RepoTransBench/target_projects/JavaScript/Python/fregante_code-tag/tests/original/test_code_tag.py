import pytest
from src.code_tag import any, html, css, gql, graphql, md, markdown, sql
import datetime

class TestConcatenateTemplateLiteralTag:
    def test_returns_raw0_when_no_keys_are_provided(self):
        # Equivalent to JS: any`Hello world!`
        assert any(["Hello world!"]) == "Hello world!"

    def test_returns_interpolated_string_when_keys_are_provided(self):
        name = "world"
        # Equivalent to any`Hello ${name}!`
        assert any(["Hello ", "!"], name) == "Hello world!"

    def test_html_alias_works_the_same_as_any(self):
        assert html(["<div>", "</div>"], 1 + 1) == "<div>2</div>"

    def test_css_alias_works_with_template_literals(self):
        assert css([".a { color: ", "; }"], "red") == ".a { color: red; }"

    def test_gql_alias_works(self):
        assert gql(["query { hello }"]) == "query { hello }"

    def test_graphql_alias_works(self):
        assert graphql(["fragment user on User { id }"]) == "fragment user on User { id }"

    def test_md_alias_works(self):
        assert md(["# Header"]) == "# Header"

    def test_markdown_alias_works(self):
        assert markdown(["* Bullet"]) == "* Bullet"

    def test_sql_alias_works(self):
        assert sql(["SELECT * FROM users WHERE id=", ""], 1) == "SELECT * FROM users WHERE id=1"

    def test_empty_template_returns_empty_string(self):
        assert any([""]) == ""

    def test_multiple_interpolations(self):
        a, b, c = "A", "B", "C"
        assert any(["", " ", " ", ""], a, b, c) == "A B C"

def test_exports_are_all_equal():
    # In JS: assert.equal(any, html); etc.
    # All should point to the same function object
    from src.code_tag import any, html, css, gql, md, sql
    functions = [any, html, css, gql, md, sql]
    assert all(f is any for f in functions)

@pytest.mark.parametrize(
    "template,values,expected",
    [
        (["a"], [], "a"),
        ([" a "], [], " a "),
        (["a", "c", ""], ["b", 1], "abc1"),
        (["\\\na\\\na"], [], "\\\na\\\na"),
        (["\\\na", ""], ["\\\na"], "\\\na\\\na"),
        (["🇪🇺 🇺🇳"], [], "🇪🇺 🇺🇳"),
        (["🇪🇺 ", ""], ["🇺🇳"], "🇪🇺 🇺🇳"),
    ]
)
def test_code_tag_various_cases(template, values, expected):
    # In JS: any`...`
    result = any(template, *values)
    assert result == expected

def test_stringifiable_objects():
    # should interpolate and use __str__ for objects
    date = datetime.datetime(2023, 1, 1, 10, 30)
    expected = str(date)
    assert any([""], date) == expected  # [""] with one value becomes str(value)