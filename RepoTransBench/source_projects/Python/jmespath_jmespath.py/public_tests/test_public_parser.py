import pytest
from jmespath.parser import Parser
from jmespath.exceptions import JMESPathTypeError, ParseError

def test_parse_valid_field_public():
    expr = 'some_other_pubfield'
    ast = Parser().parse(expr)
    assert ast.parsed['type'] == 'field'
    assert ast.parsed['value'] == 'some_other_pubfield'

def test_parse_array_projection_public():
    expr = '[*].public_special_field'
    ast = Parser().parse(expr)
    assert ast.parsed['type'] == 'projection'
    assert ast.parsed['children'][0]['type'] == 'identity'
    assert ast.parsed['children'][1]['type'] == 'field'
    assert ast.parsed['children'][1]['value'] == 'public_special_field'

def test_parse_invalid_expression_public():
    # Use a known bad construction for syntax error
    expr = '['
    # Parser.parse will raise ParseError, not JMESPathTypeError, for a syntax error
    with pytest.raises(ParseError):
        Parser().parse(expr)