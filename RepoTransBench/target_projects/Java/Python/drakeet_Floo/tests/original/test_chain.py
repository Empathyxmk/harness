def test_chain_set_and_proceed():
    called = {"val": False}

    class TestInterceptor:
        def __init__(self):
            self.called = False
        def intercept(self, chain):
            self.called = True

    class Chain:
        def __init__(self):
            self._interceptor = None
        def set_interceptor(self, interceptor):
            self._interceptor = interceptor
        def get_interceptor(self):
            return self._interceptor
        def proceed(self):
            if self._interceptor:
                self._interceptor.intercept(self)

        def set_callback(self, callback):
            self._callback = callback
        def callback(self):
            if hasattr(self, "_callback"):
                self._callback()

    chain = Chain()
    interceptor = TestInterceptor()
    chain.set_interceptor(interceptor)
    assert chain.get_interceptor() is interceptor

    chain.proceed()
    assert interceptor.called is True

def test_chain_callback():
    chain_called = {"val": False}

    class Chain:
        def set_callback(self, callback):
            self._callback = callback
        def callback(self):
            self._callback()

    chain = Chain()
    def cb():
        chain_called["val"] = True
    chain.set_callback(cb)
    chain.callback()
    assert chain_called["val"] is True

def test_chain_default_states():
    class Chain:
        def __init__(self):
            self._interceptor = None
        def get_interceptor(self):
            return self._interceptor
    chain = Chain()
    assert chain.get_interceptor() is None