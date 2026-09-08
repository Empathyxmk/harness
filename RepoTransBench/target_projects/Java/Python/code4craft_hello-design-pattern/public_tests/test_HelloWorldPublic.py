def test_HelloWorldPublic_InterfaceImpl():
    class HelloWorld:
        def helloWorld(self):
            return "different"
    hw = HelloWorld()
    assert hw.helloWorld() == "different"