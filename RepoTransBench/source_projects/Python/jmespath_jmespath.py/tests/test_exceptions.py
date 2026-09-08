import jmespath.exceptions as exceptions

def test_arity_error():
    err = exceptions.ArityError('foo', 1, 2)
    assert "ArityError" in repr(err)
    assert "foo" in str(err)

def test_parse_error():
    err = exceptions.ParseError(10, 'bad', 'ID', 'bad token')
    assert "bad" in str(err)
    assert "ID" in str(err)

def test_empty_expression_error():
    err = exceptions.EmptyExpressionError()
    assert isinstance(err, exceptions.EmptyExpressionError)

def test_variadic_arity_error():
    err = exceptions.VariadictArityError('bar', 1, 2)
    assert "VariadictArityError" in repr(err)

def test_unknown_function_error():
    err = exceptions.UnknownFunctionError("foo")
    assert "UnknownFunctionError" in repr(err)
    assert "foo" in str(err)