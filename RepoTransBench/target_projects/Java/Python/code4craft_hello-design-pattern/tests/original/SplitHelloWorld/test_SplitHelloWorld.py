def test_ToStringWithAnonymousClasses():
    class HelloWorldInterjection:
        def interjection(self):
            return "Hello"
    class HelloWorldObject:
        def object(self):
            return "World"
    class SplitHelloWorld:
        def __init__(self, interjection, obj):
            self.interjection = interjection
            self.obj = obj
        def __str__(self):
            return f"{self.interjection.interjection()} {self.obj.object()}!"
    interjection = HelloWorldInterjection()
    obj = HelloWorldObject()
    split = SplitHelloWorld(interjection, obj)
    result = str(split)
    assert "Hello" in result
    assert "World" in result