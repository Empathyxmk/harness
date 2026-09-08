def test_HelloWorldFlyWeight():
    class HelloWorld:
        def __init__(self, msg):
            self._msg = msg
        def helloWorld(self):
            return self._msg

    class HelloWorldFlyWeightFactory:
        _instance = None
        _cache = {}

        @classmethod
        def instance(cls):
            if not cls._instance:
                cls._instance = HelloWorldFlyWeightFactory()
            return cls._instance

        def createHelloWorld(self, msg):
            if msg not in self._cache:
                self._cache[msg] = HelloWorld(msg)
            return self._cache[msg]

    factory = HelloWorldFlyWeightFactory.instance()
    helloWorld = factory.createHelloWorld("Hello Flyweight!")
    assert helloWorld.helloWorld() == "Hello Flyweight!"
    helloWorld2 = factory.createHelloWorld("Hello Flyweight!")
    assert helloWorld2.helloWorld() == "Hello Flyweight!"