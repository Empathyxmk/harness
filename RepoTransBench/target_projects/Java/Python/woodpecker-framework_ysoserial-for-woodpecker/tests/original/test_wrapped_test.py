# Translated from WrappedTest.java; this is an interface, so nothing to test

def example_wrapped_test_create_callable(inner_callable):
    # inner_callable is a Callable[Object]
    def outer_callable():
        return inner_callable()
    return outer_callable