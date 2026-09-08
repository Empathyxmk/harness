def test_HelloWorldInterfaceImpl():
    class HelloWorld:
        def helloWorld(self):
            return "custom"
    hw = HelloWorld()
    assert hw.helloWorld() == "custom"