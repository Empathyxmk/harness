from unittest.mock import Mock

def test_HelloWorldObserver():
    class HelloWorldObserver:
        def __init__(self):
            self.printer = None

        def setPrinter(self, printer):
            self.printer = printer

        def update(self):
            if self.printer:
                self.printer.println("Hello Observer!")

    class Subject:
        def __init__(self):
            self._observers = []

        def attach(self, observer):
            self._observers.append(observer)
            return self

        def notifyObservers(self):
            for obs in self._observers:
                obs.update()

    observer = HelloWorldObserver()
    mock_printer = Mock()
    observer.setPrinter(mock_printer)
    subject = Subject().attach(observer)
    subject.notifyObservers()
    mock_printer.println.assert_called_once_with("Hello Observer!")