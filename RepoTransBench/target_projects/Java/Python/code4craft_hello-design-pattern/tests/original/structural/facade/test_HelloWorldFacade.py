def test_HelloWorldFacade():
    class HelloWorld:
        def helloWorld(self):
            return "Hello Facade!"

    class HelloWorldFacade:
        _inst = None

        @classmethod
        def instance(cls):
            if not cls._inst:
                cls._inst = HelloWorldFacade()
            return cls._inst

        def facadeHelloWorld(self):
            return HelloWorld()

    facadeHelloWorld = HelloWorldFacade.instance().facadeHelloWorld()
    assert facadeHelloWorld.helloWorld() == "Hello Facade!"