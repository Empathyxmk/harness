def test_HelloWorldBuilder():
    class HelloWorld:
        def __init__(self, interjection, obj):
            self._interjection = interjection
            self._object = obj
        def helloWorld(self):
            return f"{self._interjection} {self._object}!"

    class HelloWorldBuilder:
        def __init__(self):
            self._interjection = None
            self._object = None

        @classmethod
        def builder(cls):
            return HelloWorldBuilder()

        def interjection(self, interjection):
            self._interjection = interjection
            return self

        def object(self, obj):
            self._object = obj
            return self

        def getHelloWorld(self):
            return HelloWorld(self._interjection, self._object)

    builderHelloWorld = HelloWorldBuilder.builder().interjection("Hello").object("Builder").getHelloWorld()
    assert builderHelloWorld.helloWorld() == "Hello Builder!"
    helloWorld = HelloWorldBuilder.builder().interjection("Hello").object("World").getHelloWorld()
    assert helloWorld.helloWorld() == "Hello World!"