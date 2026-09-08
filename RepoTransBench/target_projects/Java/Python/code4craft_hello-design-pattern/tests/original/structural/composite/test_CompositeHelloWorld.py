def test_CompositeHelloWorld():
    class DefaultHelloWorld:
        def helloWorld(self):
            return "Hello Composite!"

    class CompositeHelloWorld:
        def __init__(self, *args):
            self.children = list(args)

        def helloWorld(self):
            return "".join(c.helloWorld() for c in self.children) if self.children else ""

    empty = CompositeHelloWorld()
    assert empty.helloWorld() == ""
    composite = CompositeHelloWorld(DefaultHelloWorld())
    assert composite.helloWorld() == "Hello Composite!"