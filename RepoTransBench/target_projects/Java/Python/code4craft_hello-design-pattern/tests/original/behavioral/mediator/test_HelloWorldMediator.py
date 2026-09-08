def test_HelloWorldMediator():
    class HelloWorldMediator:
        def __init__(self, interjection, obj):
            self.interjection = interjection
            self.obj = obj

    class HelloWorldInterjection:
        def __init__(self):
            self.mediator = None
        def setHelloWorldMediator(self, mediator):
            self.mediator = mediator
        def helloWorld(self):
            return "Hello Mediator!" if self.mediator else "No Mediator"

    class HelloWorldObject:
        def __init__(self):
            self.mediator = None
        def setHelloWorldMediator(self, mediator):
            self.mediator = mediator
        def helloWorld(self):
            return "Hello Mediator!" if self.mediator else "No Mediator"

    helloWorldInterjection = HelloWorldInterjection()
    helloWorldObject = HelloWorldObject()
    helloWorldMediator = HelloWorldMediator(helloWorldInterjection, helloWorldObject)
    helloWorldInterjection.setHelloWorldMediator(helloWorldMediator)
    helloWorldObject.setHelloWorldMediator(helloWorldMediator)
    assert helloWorldInterjection.helloWorld() == "Hello Mediator!"
    assert helloWorldObject.helloWorld() == "Hello Mediator!"