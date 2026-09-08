import pytest
from src.the_super_tiny_compiler import tokenizer, parser, transformer, codeGenerator, compiler

class TestTokenizerEdgeCasesPublic:
    def test_deeply_nested_parens_different_name(self):
        input_value = "((((bar))))"
        expected = [
            { "type": "paren", "value": "(" },
            { "type": "paren", "value": "(" },
            { "type": "paren", "value": "(" },
            { "type": "paren", "value": "(" },
            { "type": "name", "value": "bar" },
            { "type": "paren", "value": ")" },
            { "type": "paren", "value": ")" },
            { "type": "paren", "value": ")" },
            { "type": "paren", "value": ")" }
        ]
        assert tokenizer(input_value) == expected

class TestParserErrorAndEmptyHandlingPublic:
    def test_unexpected_eof_different_name(self):
        tokens = [
            { "type": "paren", "value": "(" },
            { "type": "name", "value": "fooError" }
        ]
        with pytest.raises(Exception):
            parser(tokens)

    def test_empty_input_produces_empty_program_public(self):
        assert parser([]) == { "type": "Program", "body": [] }

class TestTransformerEdgePublic:
    def test_strips_extra_program_nodes_public(self):
        ast = {
            "type": "Program",
            "body": []
        }
        expected = {
            "type": "Program",
            "body": []
        }
        assert transformer(ast) == expected

class TestCodeGeneratorPublic:
    def test_outputs_for_empty_program_public(self):
        assert codeGenerator({ "type": "Program", "body": [] }) == ""

    def test_throws_for_node_with_no_type_public(self):
        with pytest.raises(Exception):
            codeGenerator({})

    def test_number_with_leading_zeroes_different_value(self):
        ast = {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": { "type": "NumberLiteral", "value": "0052" }
                }
            ]
        }
        assert codeGenerator(ast) == "0052;"

class TestCompilerPublic:
    def test_throws_on_invalid_input_public(self):
        with pytest.raises(Exception):
            compiler("(((")
        with pytest.raises(Exception):
            compiler("&badlyFormed")