def test_HelloWorldAdapter():
    class HelloAdapterDesignPattern:
        def hello(self):
            return "Hello Adapter!"

    class HelloWorldAdapter:
        def __init__(self, adaptee):
            self.adaptee = adaptee
        def helloWorld(self):
            return self.adaptee.hello()

    adapterHelloWorld = HelloWorldAdapter(HelloAdapterDesignPattern())
    assert adapterHelloWorld.helloWorld() == "Hello Adapter!"