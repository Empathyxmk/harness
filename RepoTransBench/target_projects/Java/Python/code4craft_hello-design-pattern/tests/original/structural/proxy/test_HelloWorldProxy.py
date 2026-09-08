def test_HelloWorldFacade():
    class DefaultHelloWorld:
        def helloWorld(self):
            return "Hello Proxy!"

    class HelloWorldProxy:
        def __init__(self, delegate):
            self.delegate = delegate

        def helloWorld(self):
            return self.delegate.helloWorld()

    helloWorldProxy = HelloWorldProxy(DefaultHelloWorld())
    assert helloWorldProxy.helloWorld() == "Hello Proxy!"