def test_HelloWorldStrategyContext():
    class JavaHelloWorldStrategy:
        def helloWorld(self):
            return "Hello Java!"
    class DesignPatternHelloWorldStrategy:
        def helloWorld(self):
            return "Hello Strategy!"
    class HelloWorldStrategyContext:
        def __init__(self, strategy):
            self.strategy = strategy
        def helloWorld(self):
            return self.strategy.helloWorld()
    helloWorldStrategyContext = HelloWorldStrategyContext(JavaHelloWorldStrategy())
    assert helloWorldStrategyContext.helloWorld() == "Hello Java!"
    helloWorldStrategyContext = HelloWorldStrategyContext(DesignPatternHelloWorldStrategy())
    assert helloWorldStrategyContext.helloWorld() == "Hello Strategy!"