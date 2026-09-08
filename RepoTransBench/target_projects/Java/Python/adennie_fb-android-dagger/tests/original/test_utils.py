class DummyObjectGraph:
    def __init__(self):
        self._injected = None
    def inject(self, obj):
        self._injected = obj

class InjectingApplication:
    def __init__(self):
        self._object_graph = None
    def get_object_graph(self):
        return self._object_graph
    def inject(self, target):
        if self._object_graph:
            self._object_graph.inject(target)
    def set_object_graph(self, object_graph):
        self._object_graph = object_graph

def test_mock_injecting_application():
    app = InjectingApplication()
    obj_graph = DummyObjectGraph()
    app.set_object_graph(obj_graph)
    assert app.get_object_graph() == obj_graph
    target = object()
    app.inject(target)
    assert obj_graph._injected is target