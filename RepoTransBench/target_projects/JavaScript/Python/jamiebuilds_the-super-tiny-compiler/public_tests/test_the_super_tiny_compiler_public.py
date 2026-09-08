from src.the_super_tiny_compiler import tokenizer, parser, transformer, codeGenerator, compiler

def test_tokenizer_tokenizes_parens_name_and_numbers_different_data():
    input_value = "(multiply 3 7)"
    expected = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "multiply" },
        { "type": "number", "value": "3" },
        { "type": "number", "value": "7" },
        { "type": "paren", "value": ")" }
    ]
    assert tokenizer(input_value) == expected

def test_tokenizer_different_names_and_numbers_with_multi_digits():
    input_value = "(bar789 987foo)"
    expected = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "bar" },
        { "type": "number", "value": "789" },
        { "type": "number", "value": "987" },
        { "type": "name", "value": "foo" },
        { "type": "paren", "value": ")" }
    ]
    assert tokenizer(input_value) == expected

def test_parser_parses_basic_multiply_expression():
    tokens = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "multiply" },
        { "type": "number", "value": "3" },
        { "type": "number", "value": "7" },
        { "type": "paren", "value": ")" }
    ]
    expected = {
        "type": "Program",
        "body": [
            {
                "type": "CallExpression",
                "name": "multiply",
                "params": [
                    { "type": "NumberLiteral", "value": "3" },
                    { "type": "NumberLiteral", "value": "7" }
                ]
            }
        ]
    }
    assert parser(tokens) == expected

def test_transformer_transforms_CallExpression_to_ExpressionStatement_different_data():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "CallExpression",
                "name": "multiply",
                "params": [
                    { "type": "NumberLiteral", "value": "3" },
                    { "type": "NumberLiteral", "value": "7" }
                ]
            }
        ]
    }
    expected = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "CallExpression",
                    "callee": { "type": "Identifier", "name": "multiply" },
                    "arguments": [
                        { "type": "NumberLiteral", "value": "3" },
                        { "type": "NumberLiteral", "value": "7" }
                    ]
                }
            }
        ]
    }
    assert transformer(ast) == expected

def test_codeGenerator_generates_code_for_multiply():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "CallExpression",
                    "callee": { "type": "Identifier", "name": "multiply" },
                    "arguments": [
                        { "type": "NumberLiteral", "value": "3" },
                        { "type": "NumberLiteral", "value": "7" }
                    ]
                }
            }
        ]
    }
    assert codeGenerator(ast) == "multiply(3, 7);"

def test_codeGenerator_generates_code_for_number_different_value():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": { "type": "NumberLiteral", "value": "15" }
            }
        ]
    }
    assert codeGenerator(ast) == "15;"

def test_compiler_compiles_input_to_output_different_data():
    input_value = "(multiply 3 (divide 10 2))"
    output = "multiply(3, divide(10, 2));"
    assert compiler(input_value) == output