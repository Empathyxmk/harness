import jmespath.exceptions as exc

def test_empty_expression_error_public():
    # Must only pass self/message per code, no extra args
    err = exc.EmptyExpressionError()
    assert isinstance(err, exc.EmptyExpressionError)

def test_lexer_error_public():
    # Required signature: lex_position, lexer_value, message
    err = exc.LexerError(7, '#', "Unexpected!")
    assert err.lexer_value == '#'
    assert err.lex_position == 7
    assert "Unexpected" in str(err)

def test_parse_error_public():
    # Required signature: lex_position, token_value, message
    err = exc.ParseError(3, 'PUBSYM', "Parse oops")
    assert hasattr(err, 'token_value')
    assert err.token_value == "PUBSYM"
    assert err.lex_position == 3
    # The message is uppercased in str output, so check for that
    assert "PARSE OOPS" in str(err)

def test_arity_error_public():
    # The format places the received_args in function(), expected_args after "received"
    err = exc.ArityError("afun_pub", 2, 4)
    assert str(err) == "Expected afun_pub arguments for function 4(), received 2"

def test_variadict_arity_error_public():
    err = exc.VariadictArityError("multi_pub", 4, 9)
    assert str(err) == "Expected at least multi_pub arguments for function 9(), received 4"