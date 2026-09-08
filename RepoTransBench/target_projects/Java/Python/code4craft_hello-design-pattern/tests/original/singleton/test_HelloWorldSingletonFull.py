def test_SingletonInstance_ReturnsSameInstance():
    class HelloWorldSingleton:
        _instance = None

        @classmethod
        def instance(cls):
            if cls._instance is None:
                cls._instance = HelloWorldSingleton()
            return cls._instance

        def helloWorld(self):
            return "Hello Singleton!"

    instance1 = HelloWorldSingleton.instance()
    instance2 = HelloWorldSingleton.instance()
    assert instance1 is instance2

def test_SingletonMessage():
    class HelloWorldSingleton:
        _instance = None

        @classmethod
        def instance(cls):
            if cls._instance is None:
                cls._instance = HelloWorldSingleton()
            return cls._instance

        def helloWorld(self):
            return "Hello Singleton!"

    assert HelloWorldSingleton.instance().helloWorld() == "Hello Singleton!"