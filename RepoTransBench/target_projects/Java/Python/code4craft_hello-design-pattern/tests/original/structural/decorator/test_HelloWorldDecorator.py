def test_HelloWorldDecorator():
    class DefaultHelloWorld:
        def helloWorld(self):
            return "Hello World!"

    class HelloWorldDecorator(DefaultHelloWorld):
        def __init__(self, helloWorld):
            self._inner = helloWorld

        def helloWorld(self):
            return self._inner.helloWorld()

        def helloDecorator(self):
            return "Hello Decorator!"

    decorator = HelloWorldDecorator(DefaultHelloWorld())
    assert decorator.helloWorld() == "Hello World!"
    assert decorator.helloDecorator() == "Hello Decorator!"
    decorator2 = HelloWorldDecorator(decorator)
    assert decorator2.helloWorld() == "Hello World!"