def test_HelloWorldMediator():
    class HelloWorldMementoOriginator:
        class Memento:
            def __init__(self, state):
                self._state = state
            def get_state(self):
                return self._state
        def __init__(self):
            self.state = ""
        def set(self, state):
            self.state = state
            return self
        def helloWorld(self):
            return self.state
        def saveToMemento(self):
            return HelloWorldMementoOriginator.Memento(self.state)
        def restoreFromMemento(self, memento):
            self.state = memento.get_state()

    helloWorldMementoOriginator = HelloWorldMementoOriginator()
    memento = helloWorldMementoOriginator.set("Hello Memento!").saveToMemento()
    helloWorldMementoOriginator.set("Hello Whatever!")
    assert helloWorldMementoOriginator.helloWorld() == "Hello Whatever!"
    helloWorldMementoOriginator.restoreFromMemento(memento)
    assert helloWorldMementoOriginator.helloWorld() == "Hello Memento!"