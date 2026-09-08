import pytest
from src.the_super_tiny_compiler import tokenizer, parser, transformer, codeGenerator, compiler

class TestTokenizerEdgeCases:
    def test_deeply_nested_parens(self):
        input_value = "(((foo)))"
        expected = [
            { "type": "paren", "value": "(" },
            { "type": "paren", "value": "(" },
            { "type": "paren", "value": "(" },
            { "type": "name", "value": "foo" },
            { "type": "paren", "value": ")" },
            { "type": "paren", "value": ")" },
            { "type": "paren", "value": ")" }
        ]
        assert tokenizer(input_value) == expected

class TestParserErrorAndEmptyHandling:
    def test_unexpected_eof(self):
        tokens = [
            { "type": "paren", "value": "(" },
            { "type": "name", "value": "oops" }
        ]
        with pytest.raises(Exception):
            parser(tokens)

    def test_empty_input_produces_empty_program(self):
        assert parser([]) == { "type": "Program", "body": [] }

class TestTransformerEdge:
    def test_strips_extra_program_nodes(self):
        ast = {
            "type": "Program",
            "body": []
        }
        expected = {
            "type": "Program",
            "body": []
        }
        assert transformer(ast) == expected

class TestCodeGenerator:
    def test_outputs_for_empty_program(self):
        assert codeGenerator({ "type": "Program", "body": [] }) == ""

    def test_throws_for_node_with_no_type(self):
        with pytest.raises(Exception):
            codeGenerator({})

    def test_number_with_leading_zeroes(self):
        ast = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": { "type": "NumberLiteral", "value": "007" }
                }
            ]
        }
        assert codeGenerator(ast) == "007;"

class TestCompiler:
    def test_throws_on_invalid_input(self):
        with pytest.raises(Exception):
            compiler("(")
        with pytest.raises(Exception):
            compiler("$foo")