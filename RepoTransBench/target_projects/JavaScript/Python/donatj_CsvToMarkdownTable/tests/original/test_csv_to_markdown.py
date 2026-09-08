import pytest
from src.csv_to_markdown import csv_to_markdown

def test_should_return_headers_and_blank_row_for_empty_input():
    result = csv_to_markdown("")
    assert result == "|  | \n|--| \n|  | \n"

def test_should_return_table_with_blank_headers_using_default_settings():
    result = csv_to_markdown("a\tb\tc")
    assert result == "|   |   |   | \n|---|---|---| \n| a | b | c | \n"

def test_should_handle_windows_newlines_gracefully():
    result = csv_to_markdown("a\tb\r\nc\td\r\ne\tf\r\n", "\t", True)
    assert result == "| a | b | \n|---|---| \n| c | d | \n| e | f | \n|   |   | \n"

def test_should_return_table_with_no_headers():
    result = csv_to_markdown("a\tb\tc", "\t", False)
    assert result == "|   |   |   | \n|---|---|---| \n| a | b | c | \n"

def test_should_return_table_with_headers_and_no_data():
    result = csv_to_markdown("a\tb\tc", "\t", True)
    assert result == "| a | b | c | \n|---|---|---| \n"

def test_should_return_table_with_blank_headers_various_separators():
    cases = [("a\tb\tc", "\t"), ("a,b,c", ","), ("a;b;c", ";")]
    for inp, delim in cases:
        result = csv_to_markdown(inp, delim, False)
        assert result == "|   |   |   | \n|---|---|---| \n| a | b | c | \n"

def test_should_contain_separator_when_in_quotes():
    cases = [("a\t\"b\tc\"\td", "\t"), ("a,\"b,c\",d", ","), ("a;\"b;c\";d", ";")]
    for inp, delim in cases:
        result = csv_to_markdown(inp, delim, False)
        # Compose the expectation with quoted separator and padding
        assert result == f"|   |       |   | \n|---|-------|---| \n| a | \"b{delim}c\" | d | \n"

def test_should_return_table_with_headers_and_no_data_again():
    result = csv_to_markdown("a\tb\tc", "\t", True)
    assert result == "| a | b | c | \n|---|---|---| \n"

def test_should_convert_tabs_to_four_spaces_for_github():
    result = csv_to_markdown("a\tb\tc", ";", False)
    assert result == "|             | \n|-------------| \n| a    b    c | \n"

def test_should_format_with_semicolons_and_long_values():
    result = csv_to_markdown("a;b;c;long value\nd;e;f", ";", False)
    assert result == "|   |   |   |            | \n|---|---|---|------------| \n| a | b | c | long value | \n| d | e | f |            | \n"

def test_should_skip_delimiters_wrapped_by_quotes():
    result = csv_to_markdown('"a, b, c, d",e', ",", False)
    assert result == '|              |   | \n|--------------|---| \n| "a, b, c, d" | e | \n'

def test_should_escape_pipes_and_backslashes():
    result = csv_to_markdown('"a|b|c|d",e\\f\\g', ",", False)
    assert result == '|              |         | \n|--------------|---------| \n| "a\\|b\\|c\\|d" | e\\\\f\\\\g | \n'

def test_should_handle_single_values_ending_in_delimiter():
    result = csv_to_markdown('"assd;"', ";", False)
    assert result == '|         | \n|---------| \n| "assd;" | \n'

def test_should_handle_items_begin_with_word_boundaries():
    result = csv_to_markdown('"foo";"bar";"baz"\n"1";"2";"[foo -;- bar baz]"', ";", True)
    assert result == '| "foo" | "bar" | "baz"               | \n|-------|-------|---------------------| \n| "1"   | "2"   | "[foo -;- bar baz]" | \n'

def test_should_handle_delimiters_that_are_regex_special_chars():
    delimiters = ['[', ']', '\\', '/', '^', '$', '.', '|', '?', '*', '+', '(', ')', '{', '}', '-']
    for delimiter in delimiters:
        result = csv_to_markdown('a' + delimiter + 'b' + delimiter + 'c', delimiter, False)
        assert result == '|   |   |   | \n|---|---|---| \n| a | b | c | \n'