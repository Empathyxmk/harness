def test_HelloWorldPrototype():
    class HelloWorld:
        def helloWorld(self):
            return "Hello Prototype!"

    class HelloWorldPrototype(HelloWorld):
        PROTOTYPE = None

        def __init__(self):
            super().__init__()

        def clone(self):
            return HelloWorldPrototype()

        def helloWorld(self):
            return "Hello Prototype!"

    HelloWorldPrototype.PROTOTYPE = HelloWorldPrototype()

    helloWorld = HelloWorldPrototype.PROTOTYPE.clone()
    assert helloWorld.helloWorld() == "Hello Prototype!"