import pytest

class LoggingManager:
    pass

class DummyObjectGraph:
    def __init__(self):
        self.plus_args = None
        self.injected = []
    def plus(self, *args):
        self.plus_args = args
        return self
    def inject(self, obj):
        self.injected.append(obj)

class DummyInjector:
    def __init__(self, obj_graph):
        self._object_graph = obj_graph
    def get_object_graph(self):
        return self._object_graph
    def inject(self, target):
        self._object_graph.inject(target)

class InjectingPreferenceFragment:
    def __init__(self):
        self._object_graph = None
        self._first_attach = True
        self._attach_calls = 0
        self._destroy_calls = 0
        self._modules = None
    def get_object_graph(self):
        return self._object_graph
    def get_modules(self):
        # For public: LoggingManager
        if self._modules is None:
            self._modules = [LoggingManager()]
        return self._modules
    def on_attach(self, activity):
        modules = self.get_modules()
        self._object_graph = activity.get_object_graph().plus(*modules)
        if self._first_attach:
            self._object_graph.inject(self)
            self._first_attach = False
        self._attach_calls += 1
    def on_destroy(self):
        self._object_graph = None
        self._destroy_calls += 1
    def inject(self, target):
        if not self._object_graph:
            raise IllegalStateException("Graph not initialized")
        self._object_graph.inject(target)

class IllegalStateException(Exception):
    pass

def test_on_attach_first_time_public():
    fragment = InjectingPreferenceFragment()
    obj_graph = DummyObjectGraph()
    fragment_obj_graph = DummyObjectGraph()
    class Activity(DummyInjector):
        def get_object_graph(self):
            return obj_graph
    activity = Activity(obj_graph)
    obj_graph.plus = lambda *args: fragment_obj_graph
    fragment_obj_graph.inject = lambda target: setattr(fragment, "_injected", [target])
    fragment.on_attach(activity)
    assert fragment.get_object_graph() is fragment_obj_graph
    assert getattr(fragment, "_injected", None) == [fragment]
    assert fragment._attach_calls == 1

def test_on_attach_retained_fragment_public():
    fragment = InjectingPreferenceFragment()
    obj_graph = DummyObjectGraph()
    fragment_obj_graph = DummyObjectGraph()
    class Activity(DummyInjector):
        def get_object_graph(self):
            return obj_graph
    activity = Activity(obj_graph)
    obj_graph.plus = lambda *args: fragment_obj_graph
    call_count = [0]
    def inject(target):
        call_count[0] += 1
        fragment._injected = [target]
    fragment_obj_graph.inject = inject
    fragment.on_attach(activity)
    assert call_count[0] == 1
    fragment._first_attach = False
    call_count[0] = 0
    fragment.on_attach(activity)
    assert call_count[0] == 0
    assert fragment._attach_calls == 2

def test_on_destroy_public():
    fragment = InjectingPreferenceFragment()
    obj_graph = DummyObjectGraph()
    fragment_obj_graph = DummyObjectGraph()
    class Activity(DummyInjector):
        def get_object_graph(self):
            return obj_graph
    activity = Activity(obj_graph)
    obj_graph.plus = lambda *args: fragment_obj_graph
    fragment_obj_graph.inject = lambda target: None
    fragment.on_attach(activity)
    assert fragment.get_object_graph() is not None
    fragment.on_destroy()
    assert fragment.get_object_graph() is None
    assert fragment._destroy_calls == 1

def test_get_object_graph_public():
    fragment = InjectingPreferenceFragment()
    obj_graph = DummyObjectGraph()
    fragment_obj_graph = DummyObjectGraph()
    class Activity(DummyInjector):
        def get_object_graph(self):
            return obj_graph
    activity = Activity(obj_graph)
    obj_graph.plus = lambda *a: fragment_obj_graph
    fragment_obj_graph.inject = lambda target: None
    fragment.on_attach(activity)
    assert fragment.get_object_graph() is fragment_obj_graph

def test_inject_graph_initialized_public():
    fragment = InjectingPreferenceFragment()
    obj_graph = DummyObjectGraph()
    fragment_obj_graph = DummyObjectGraph()
    class Activity(DummyInjector):
        def get_object_graph(self):
            return obj_graph
    activity = Activity(obj_graph)
    obj_graph.plus = lambda *a: fragment_obj_graph
    called = dict(val=False)
    def inject(target):
        called['val'] = target
    fragment_obj_graph.inject = inject
    fragment.on_attach(activity)
    target = "MyInjectedTarget"
    fragment.inject(target)
    assert called['val'] == target

def test_inject_graph_not_initialized_public():
    fragment = InjectingPreferenceFragment()
    with pytest.raises(IllegalStateException):
        fragment.inject(999)

def test_get_modules_public():
    fragment = InjectingPreferenceFragment()
    modules = fragment.get_modules()
    assert modules is not None
    assert len(modules) == 1
    assert isinstance(modules[0], LoggingManager)