def test_HelloWorldVisitor():
    class HelloWorldCharacterVisitor:
        def __init__(self):
            self.result = []

        def visit(self, char_element):
            self.result.append(char_element)

        def helloWorld(self):
            return "".join(self.result)

    class HelloWorldCharacterElements:
        def __init__(self, chars):
            self.chars = chars

        def accept(self, visitor):
            for c in self.chars:
                visitor.visit(c)

    elements = HelloWorldCharacterElements("Hello Visitor!")
    visitor = HelloWorldCharacterVisitor()
    elements.accept(visitor)
    assert visitor.helloWorld() == "Hello Visitor!"