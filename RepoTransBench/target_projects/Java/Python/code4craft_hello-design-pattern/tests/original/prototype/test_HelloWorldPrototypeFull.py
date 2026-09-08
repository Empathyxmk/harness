import pytest

class HelloWorld:
    def helloWorld(self):
        raise NotImplementedError

class HelloWorldPrototype(HelloWorld):
    PROTOTYPE = None  # Set after class definition

    def __init__(self, message=None):
        self._message = message or "Hello Prototype!"

    def clone(self):
        return HelloWorldPrototype(self._message)

    def helloWorld(self):
        return self._message

HelloWorldPrototype.PROTOTYPE = HelloWorldPrototype()

def test_HelloWorldPrototype_CloneAndMessage():
    proto = HelloWorldPrototype("Test Prototype!")
    cloned = proto.clone()
    assert isinstance(cloned, HelloWorldPrototype)
    assert cloned.helloWorld() == "Test Prototype!"

def test_HelloWorldPrototype_Constant():
    assert HelloWorldPrototype.PROTOTYPE.helloWorld() == "Hello Prototype!"
    copy = HelloWorldPrototype.PROTOTYPE.clone()
    assert isinstance(copy, HelloWorldPrototype)
    assert copy.helloWorld() == "Hello Prototype!"