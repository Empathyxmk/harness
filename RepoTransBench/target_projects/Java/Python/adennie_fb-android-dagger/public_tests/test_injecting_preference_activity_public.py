import pytest

class LoggingManager:
    pass

class DummyObjectGraph:
    def __init__(self):
        self.plus_called = False
        self.injected = []
    def plus(self, *args):
        self.plus_called = True
        return self
    def inject(self, target):
        self.injected.append(target)

class InjectingActivityModule:
    def __init__(self, activity, injector):
        self.activity = activity
        self.injector = injector

class DummyApplication:
    def __init__(self, obj_graph):
        self._object_graph = obj_graph
    def get_object_graph(self):
        return self._object_graph
    def inject(self, target):
        self._object_graph.inject(target)

class InjectingPreferenceActivity:
    def __init__(self):
        self._object_graph = None
        self._on_create_calls = 0
        self._on_destroy_calls = 0
        self._application = None
        self._modules = None
    def set_application(self, app):
        self._application = app
    def get_application(self):
        return self._application
    def get_object_graph(self):
        return self._object_graph
    def get_modules(self):
        if self._modules is None:
            self._modules = [
                InjectingActivityModule(self, self),
                LoggingManager()
            ]
        return self._modules
    def on_create(self, bundle):
        app = self.get_application()
        self._object_graph = app.get_object_graph().plus(*self.get_modules())
        self._object_graph.inject(self)
        self._on_create_calls += 1
    def on_destroy(self):
        self._object_graph = None
        self._on_destroy_calls += 1
    def inject(self, target):
        if self._object_graph is None:
            raise IllegalStateException("Object graph not initialized")
        self._object_graph.inject(target)

class IllegalStateException(Exception):
    pass

def test_on_create_public():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingPreferenceActivity()
    activity.set_application(app)
    assert activity.get_object_graph() is None
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph
    assert activity._on_create_calls == 1
    assert activity in obj_graph.injected

def test_on_destroy_public():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingPreferenceActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph
    activity.on_destroy()
    assert activity.get_object_graph() is None
    assert activity._on_destroy_calls == 1

def test_get_object_graph_public():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingPreferenceActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    assert activity.get_object_graph() == obj_graph

def test_inject_graph_initialized_public():
    obj_graph = DummyObjectGraph()
    app = DummyApplication(obj_graph)
    activity = InjectingPreferenceActivity()
    activity.set_application(app)
    activity.on_create(bundle={})
    target = "AnotherTarget"
    activity.inject(target)
    assert target in obj_graph.injected

def test_inject_graph_not_initialized_public():
    activity = InjectingPreferenceActivity()
    with pytest.raises(IllegalStateException):
        activity.inject(0.01)

def test_get_modules_public():
    activity = InjectingPreferenceActivity()
    modules = activity.get_modules()
    assert modules is not None
    assert len(modules) == 2
    assert isinstance(modules[0], InjectingActivityModule)
    assert isinstance(modules[1], LoggingManager)