def test_HelloWorldSingleton():
    class HelloWorld:
        def helloWorld(self):
            return "Hello Singleton!"

    class HelloWorldSingleton(HelloWorld):
        _instance = None

        @classmethod
        def instance(cls):
            if not cls._instance:
                cls._instance = HelloWorldSingleton()
            return cls._instance

    helloWorld = HelloWorldSingleton.instance()
    assert helloWorld.helloWorld() == "Hello Singleton!"