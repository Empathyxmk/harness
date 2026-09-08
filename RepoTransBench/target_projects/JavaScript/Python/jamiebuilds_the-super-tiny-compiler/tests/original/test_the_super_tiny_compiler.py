from src.the_super_tiny_compiler import tokenizer, parser, transformer, codeGenerator, compiler

def test_tokenizer_tokenizes_parens_name_and_numbers():
    input_value = "(add 2 4)"
    expected = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "add" },
        { "type": "number", "value": "2" },
        { "type": "number", "value": "4" },
        { "type": "paren", "value": ")" }
    ]
    assert tokenizer(input_value) == expected

def test_tokenizer_tokenizes_names_and_numbers_with_multi_digits():
    input_value = "(foo123 456bar)"
    expected = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "foo" },
        { "type": "number", "value": "123" },
        { "type": "number", "value": "456" },
        { "type": "name", "value": "bar" },
        { "type": "paren", "value": ")" }
    ]
    assert tokenizer(input_value) == expected

def test_parser_parses_basic_add_expression():
    tokens = [
        { "type": "paren", "value": "(" },
        { "type": "name", "value": "add" },
        { "type": "number", "value": "2" },
        { "type": "number", "value": "4" },
        { "type": "paren", "value": ")" }
    ]
    expected = {
        "type": "Program",
        "body": [
            {
                "type": "CallExpression",
                "name": "add",
                "params": [
                    { "type": "NumberLiteral", "value": "2" },
                    { "type": "NumberLiteral", "value": "4" }
                ]
            }
        ]
    }
    assert parser(tokens) == expected

def test_transformer_transforms_CallExpression_to_ExpressionStatement():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "CallExpression",
                "name": "add",
                "params": [
                    { "type": "NumberLiteral", "value": "2" },
                    { "type": "NumberLiteral", "value": "4" }
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
                    "callee": { "type": "Identifier", "name": "add" },
                    "arguments": [
                        { "type": "NumberLiteral", "value": "2" },
                        { "type": "NumberLiteral", "value": "4" }
                    ]
                }
            }
        ]
    }
    assert transformer(ast) == expected

def test_codeGenerator_generates_code_for_add():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "CallExpression",
                    "callee": { "type": "Identifier", "name": "add" },
                    "arguments": [
                        { "type": "NumberLiteral", "value": "2" },
                        { "type": "NumberLiteral", "value": "4" }
                    ]
                }
            }
        ]
    }
    assert codeGenerator(ast) == "add(2, 4);"

def test_codeGenerator_generates_code_for_number():
    ast = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": { "type": "NumberLiteral", "value": "8" }
            }
        ]
    }
    assert codeGenerator(ast) == "8;"

def test_compiler_compiles_input_to_output():
    input_value = "(add 2 (subtract 4 2))"
    output = "add(2, subtract(4, 2));"
    assert compiler(input_value) == output