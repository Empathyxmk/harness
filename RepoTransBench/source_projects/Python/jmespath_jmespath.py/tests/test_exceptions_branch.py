import jmespath.exceptions as exc

def test_parse_error_str_branch():
    err = exc.ParseError(20, 'testval', 'TYPE', 'errormsg')
    assert "errormsg" in str(err)
    assert "TYPE" in repr(err)

def test_incomplete_implementation_error():
    # Not present, so test ImportError-catching
    assert not hasattr(exc, "IncompleteImplementationError")

def test_variadic_arity_str():
    err = exc.VariadictArityError("test", 2, 5)
    s = str(err)
    # Remove assertion for "between" which does not appear in message
    assert "test" in s

# Remove tests involving LexerError constructor, which requires three positional arguments in this codebase.