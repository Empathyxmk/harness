from datetime import datetime, timedelta
import json

import jmespath
from jmespath import exceptions


def test_can_max_datetimes_different():
    data = [datetime(2020, 7, 1, 12, 0, 0), datetime(2020, 7, 1, 12, 0, 3)]
    result = jmespath.search('max([*].to_string(@))', data)
    assert json.loads(result) == str(data[-1])


def test_type_error_messages_variant():
    # length() applied to a boolean
    try:
        jmespath.search('length(@)', True)
    except exceptions.JMESPathTypeError as e:
        msg = str(e)
        assert 'length()' in msg
        assert 'invalid type for value: True' in msg
        assert "expected one of: ['string', 'array', 'object']" in msg
        assert 'received: "boolean"' in msg
    else:
        assert False, "Expected JMESPathTypeError"


def test_singular_in_error_message_variant():
    # Give 3 args to a function expecting 1
    try:
        jmespath.search('length(@, @, @)', [0, 1, 2])
    except exceptions.ArityError as e:
        assert str(e) == 'Expected 1 argument for function length(), received 3'
    else:
        assert False, "Expected ArityError"


def test_error_message_is_pluralized_variant():
    # Give 0 args to a function expecting 2
    try:
        jmespath.search('sort_by()', [])
    except exceptions.ArityError as e:
        assert str(e) == 'Expected 2 arguments for function sort_by(), received 0'
    else:
        assert False, "Expected ArityError"


def test_variadic_is_pluralized_variant():
    # No args for not_null (should expect at least 1)
    try:
        jmespath.search('not_null()', [])
    except exceptions.VariadictArityError as e:
        assert str(e) == 'Expected at least 1 argument for function not_null(), received 0'
    else:
        assert False, "Expected VariadictArityError"