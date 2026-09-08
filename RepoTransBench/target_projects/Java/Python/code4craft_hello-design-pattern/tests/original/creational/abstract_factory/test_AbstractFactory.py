def test_AbstractFactory():
    class JavaObject:
        def object(self):
            return "Java"
    class JavaInterjection:
        def interjection(self):
            return "Hello"
    class DPObject:
        def object(self):
            return "Abstract Factory"
    class DPInterjection:
        def interjection(self):
            return "Hello"
    class AbstractFactory:
        class Type:
            Java = 0
            DesignPattern = 1

        @staticmethod
        def select(type_):
            if type_ == AbstractFactory.Type.Java:
                return JavaSplitHelloWorldFactory()
            if type_ == AbstractFactory.Type.DesignPattern:
                return DesignPatternSplitHelloWorldFactory()
            raise ValueError()
    class JavaSplitHelloWorldFactory:
        def createHelloWorldObject(self):
            return JavaObject()
        def createHelloWorldInterjection(self):
            return JavaInterjection()
    class DesignPatternSplitHelloWorldFactory:
        def createHelloWorldObject(self):
            return DPObject()
        def createHelloWorldInterjection(self):
            return DPInterjection()
    splitHelloWorldFactory = AbstractFactory.select(AbstractFactory.Type.Java)
    assert splitHelloWorldFactory.createHelloWorldObject().object() == "Java"
    assert splitHelloWorldFactory.createHelloWorldInterjection().interjection() == "Hello"
    splitHelloWorldFactory = AbstractFactory.select(AbstractFactory.Type.DesignPattern)
    assert splitHelloWorldFactory.createHelloWorldInterjection().interjection() == "Hello"
    assert splitHelloWorldFactory.createHelloWorldObject().object() == "Abstract Factory"