def test_FactoryMethodHelloWorldFactory():
    class HelloWorld:
        def helloWorld(self):
            return "Hello World!"
    class HelloWorldFactory:
        def createHelloWorld(self):
            return HelloWorld()
    class FactoryMethodHelloWorldFactory:
        def createHelloWorld(self):
            class FactoryHelloWorld:
                def helloWorld(self2):
                    return "Hello Factory Method!"
            return FactoryHelloWorld()
    helloWorldFactory = HelloWorldFactory()
    helloWorld = helloWorldFactory.createHelloWorld()
    assert helloWorld.helloWorld() == "Hello World!"
    factoryMethodHelloWorldFactory = FactoryMethodHelloWorldFactory()
    helloWorld = factoryMethodHelloWorldFactory.createHelloWorld()
    assert helloWorld.helloWorld() == "Hello Factory Method!"