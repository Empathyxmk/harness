def test_default_constructor_sets_no_message_or_cause():
    class NoOrderException(Exception):
        pass

    ex = NoOrderException()
    assert ex.args == ()