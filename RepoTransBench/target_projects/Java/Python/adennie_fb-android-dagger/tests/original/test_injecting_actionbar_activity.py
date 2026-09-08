import pytest

class DummyObjectGraph:
    def __init__(self):
        self.plus_args = None
        self.injected = []
    def plus(self, *args):
        self.plus_args = args
        return self
    def inject(self, target):
        self.injected.append(target)

class DummyApplication:
    def __init__(self, object_graph):
        self._object_graph = object_graph
    def get_object_graph(self):
        return self._object_graph
    def inject(self, target):
        self._object_graph.inject(target)

class InjectingActivityModule:
    def __init__(self, activity, injector):
        self.activity = activity
        self.injector = injector

class InjectingActionBarActivity:
    def __init__(self):
        self._object_graph = None
        self._on_create_count = 0
        self._on_destroy_count = 0
        self._modules = None
        self._application = None
    def set_application(self, app):
        self._application = app
    def get_application(self):
        return self._application
    def get_object_graph(self):
        return self._object_graph
    def get_modules(self):
        if self._modules is None:
            self._modules = [InjectingActivityModule(self, self)]
        return self._modules
    def on_create(self, bundle):
        app = self.get_application()
        self._object_graph = app.get_object_graph().plus(*self.get_modules())
        self._object_graph.inject(self)
        self._on_create_count += 1
    def on_destroy(self):
        self._object_graph = None
        self._on_destroy_count += 1
    def inject(self, target):
        if self._object_graph is None:
            raise IllegalStateException("Object graph not initialized")
        self._object_graph.inject(target)

class IllegalStateException(Exception):
    pass

def test_on_create():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingActionBarActivity()
    activity.set_application(app)
    assert activity.get_object_graph() is None
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph
    assert activity._on_create_count == 1
    assert activity in obj_graph.injected

def test_on_destroy():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingActionBarActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph
    activity.on_destroy()
    assert activity.get_object_graph() is None
    assert activity._on_destroy_count == 1

def test_get_object_graph():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingActionBarActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph

def test_inject_graph_initialized():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingActionBarActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    target = object()
    activity.inject(target)
    assert target in obj_graph.injected

def test_inject_graph_not_initialized():
    activity = InjectingActionBarActivity()
    with pytest.raises(IllegalStateException):
        activity.inject(object())

def test_get_modules():
    activity = InjectingActionBarActivity()
    modules = activity.get_modules()
    assert modules is not None
    assert len(modules) == 1
    assert isinstance(modules[0], InjectingActivityModule)