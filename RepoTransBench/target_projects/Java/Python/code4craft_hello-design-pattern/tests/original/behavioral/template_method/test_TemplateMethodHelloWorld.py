def test_TemplateMethodHelloWorld():
    class TemplateMethodHelloWorld:
        def helloWorld(self):
            return "Hello Template Method!"

    templateMethodHelloWorld = TemplateMethodHelloWorld()
    assert templateMethodHelloWorld.helloWorld() == "Hello Template Method!"