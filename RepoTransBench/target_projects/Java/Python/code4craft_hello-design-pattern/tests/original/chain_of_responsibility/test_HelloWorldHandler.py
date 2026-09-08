def test_ConcreteHandler():
    class HelloWorldHandler:
        def handle(self, buffer):
            raise NotImplementedError()

    class ConcreteHelloWorldHandler(HelloWorldHandler):
        def handle(self, buffer):
            buffer.append("Handled")

    buf = []
    handler = ConcreteHelloWorldHandler()
    handler.handle(buf)
    assert "".join(buf) == "Handled"