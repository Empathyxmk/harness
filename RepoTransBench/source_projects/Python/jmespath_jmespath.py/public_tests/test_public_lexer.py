import jmespath.lexer as lexer

def test_tokenize_identifier_public():
    lex = lexer.Lexer()
    tokens = list(lex.tokenize("ABC_2024_pub"))
    assert tokens[0]['type'] == 'unquoted_identifier'
    assert tokens[0]['value'] == 'ABC_2024_pub'
    assert tokens[-1]['type'] == 'eof'

def test_tokenize_number_public():
    lex = lexer.Lexer()
    tokens = list(lex.tokenize("2468013"))
    assert any(t['type'] == 'number' for t in tokens)

def test_tokenize_operator_public():
    # Check that 'gt', 'lt', 'ne', 'eq' get emitted for these operators
    lex = lexer.Lexer()
    tokens = list(lex.tokenize("> < != =="))
    types = [t['type'] for t in tokens if t['type'] != 'eof']
    assert 'gt' in types
    assert 'lt' in types
    assert 'ne' in types
    assert 'eq' in types
    assert tokens[-1]['type'] == 'eof'