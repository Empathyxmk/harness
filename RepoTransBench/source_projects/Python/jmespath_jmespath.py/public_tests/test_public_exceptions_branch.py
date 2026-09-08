import jmespath.exceptions as exc

def test_empty_expression_error_public_branch():
    # Only instantiate, check type
    err = exc.EmptyExpressionError()
    assert isinstance(err, exc.EmptyExpressionError)

def test_parse_error_public_branch():
    # Use alternate tokens/values for parse error
    err = exc.ParseError(5, 'BRANCHPUB', "Branchparse issue")
    assert err.token_value == "BRANCHPUB"
    assert err.lex_position == 5
    # The message appears uppercased in str output
    assert "BRANCHPARSE ISSUE" in str(err)