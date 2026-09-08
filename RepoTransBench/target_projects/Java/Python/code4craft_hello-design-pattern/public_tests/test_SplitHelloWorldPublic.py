def test_ToStringWithAnonymousClasses_Public():
    class HelloWorldInterjection:
        def interjection(self):
            return "Hi"
    class HelloWorldObject:
        def object(self):
            return "Universe"
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
    assert "Hi" in result
    assert "Universe" in result