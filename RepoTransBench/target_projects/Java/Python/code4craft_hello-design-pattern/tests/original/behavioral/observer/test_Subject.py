def test_AttachAndNotify():
    class Observer:
        def update(self):
            pass
    class DummyObserver(Observer):
        def __init__(self):
            self.updated = False
        def update(self):
            self.updated = True
    class Subject:
        def __init__(self):
            self._observers = []
        def attach(self, observer):
            self._observers.append(observer)
            return self
        def notifyObservers(self):
            for o in self._observers:
                o.update()
    subject = Subject()
    obs = DummyObserver()
    subject.attach(obs)
    subject.notifyObservers()
    assert obs.updated