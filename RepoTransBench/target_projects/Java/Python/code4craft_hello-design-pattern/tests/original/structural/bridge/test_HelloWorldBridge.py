def test_HelloWorldAdapter():
    class JavaHelloWorldImpl:
        def helloWorld(self):
            return "Hello Java!"

    class DesignPatternWorldImpl:
        def helloWorld(self):
            return "Hello Bridge!"

    class HelloWorldBridge:
        def __init__(self, impl):
            self.impl = impl
        def helloWorld(self):
            return self.impl.helloWorld()

    bridgeHelloWorld = HelloWorldBridge(JavaHelloWorldImpl())
    assert bridgeHelloWorld.helloWorld() == "Hello Java!"
    bridgeHelloWorld = HelloWorldBridge(DesignPatternWorldImpl())
    assert bridgeHelloWorld.helloWorld() == "Hello Bridge!"