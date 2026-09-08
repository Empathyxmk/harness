import pytest
from unittest import mock

class DummyObjectGraph:
    def __init__(self):
        self.inject_called_with = []
    def plus(self, *args):
        return self
    def inject(self, target):
        self.inject_called_with.append(target)

class DummyInjector:
    def __init__(self, obj_graph):
        self._obj_graph = obj_graph
    def get_object_graph(self):
        return self._obj_graph
    def inject(self, obj):
        self._obj_graph.inject(obj)

class InjectingFragmentModule:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class InjectingPreferenceFragment:
    def __init__(self):
        self._object_graph = None
        self._first_attach = True
        self._injected = []
    def get_object_graph(self):
        return self._object_graph
    def on_attach(self, activity):
        injector = activity
        modules = self.get_modules()
        self._object_graph = injector.get_object_graph().plus(*modules)
        if self._first_attach:
            self._object_graph.inject(self)
            self._first_attach = False
        # Simulate super().on_attach by marking call count
        if hasattr(self, "_attach_call_count"):
            self._attach_call_count += 1
        else:
            self._attach_call_count = 1
    def on_destroy(self):
        self._object_graph = None
        if hasattr(self, "_destroy_call_count"):
            self._destroy_call_count += 1
        else:
            self._destroy_call_count = 1
    def inject(self, target):
        if not self._object_graph:
            raise IllegalStateException("Object graph not initialized")
        self._object_graph.inject(target)
    def get_modules(self):
        return [InjectingFragmentModule(self, self)]
    # for spy: count super calls for verification
    def __getattr__(self, attr):
        # for on_attach and on_destroy
        if attr == "on_attach":
            def call(*args, **kwargs):
                if hasattr(self, "_attach_call_count"):
                    self._attach_call_count += 1
                else:
                    self._attach_call_count = 1
            return call
        if attr == "on_destroy":
            def call(*args, **kwargs):
                if hasattr(self, "_destroy_call_count"):
                    self._destroy_call_count += 1
                else:
                    self._destroy_call_count = 1
            return call
        raise AttributeError(attr)

class IllegalStateException(Exception):
    pass

def test_on_attach_first_time(monkeypatch):
    fragment = InjectingPreferenceFragment()
    assert fragment.get_object_graph() is None

    # Mocks
    mock_activity_obj_graph = DummyObjectGraph()
    mock_fragment_obj_graph = DummyObjectGraph()
    class MockActivity(DummyInjector):
        def get_object_graph(self):
            return mock_activity_obj_graph
    activity = MockActivity(mock_activity_obj_graph)
    def plus(modules):
        return mock_fragment_obj_graph
    monkeypatch.setattr(mock_activity_obj_graph, 'plus', lambda *a: mock_fragment_obj_graph)
    monkeypatch.setattr(mock_fragment_obj_graph, 'inject', lambda target: setattr(fragment, "_injected", [target]))
    fragment.get_modules = lambda: [InjectingFragmentModule(fragment, fragment)]

    fragment.on_attach(activity)
    assert fragment.get_object_graph() == mock_fragment_obj_graph
    assert fragment._injected == [fragment]
    assert getattr(fragment, "_attach_call_count", 1) == 1

def test_on_attach_retained_fragment(monkeypatch):
    fragment = InjectingPreferenceFragment()
    mock_activity_obj_graph = DummyObjectGraph()
    mock_fragment_obj_graph = DummyObjectGraph()
    class MockActivity(DummyInjector):
        def get_object_graph(self):
            return mock_activity_obj_graph
    activity = MockActivity(mock_activity_obj_graph)
    monkeypatch.setattr(mock_activity_obj_graph, 'plus', lambda *a: mock_fragment_obj_graph)
    fragment.get_modules = lambda: [InjectingFragmentModule(fragment, fragment)]
    inject_call_counter = [0]
    def inject(target):
        inject_call_counter[0] += 1
        fragment._injected = [target]
    monkeypatch.setattr(mock_fragment_obj_graph, 'inject', inject)

    fragment.on_attach(activity)
    assert inject_call_counter[0] == 1
    # Simulate retained: set first_attach to False
    fragment._first_attach = False
    inject_call_counter[0] = 0

    fragment.on_attach(activity)
    assert inject_call_counter[0] == 0
    assert fragment.get_object_graph() == mock_fragment_obj_graph
    assert getattr(fragment, "_attach_call_count", 2) == 2

def test_on_destroy():
    fragment = InjectingPreferenceFragment()
    mock_activity_obj_graph = DummyObjectGraph()
    mock_fragment_obj_graph = DummyObjectGraph()
    class MockActivity(DummyInjector):
        def get_object_graph(self):
            return mock_activity_obj_graph
    activity = MockActivity(mock_activity_obj_graph)
    fragment.get_modules = lambda: [InjectingFragmentModule(fragment, fragment)]
    mock_activity_obj_graph.plus = lambda *a: mock_fragment_obj_graph
    mock_fragment_obj_graph.inject = lambda target: None
    fragment.on_attach(activity)
    assert fragment.get_object_graph() is not None
    fragment.on_destroy()
    assert fragment.get_object_graph() is None
    assert getattr(fragment, "_destroy_call_count", 1) == 1

def test_get_object_graph():
    fragment = InjectingPreferenceFragment()
    mock_activity_obj_graph = DummyObjectGraph()
    mock_fragment_obj_graph = DummyObjectGraph()
    class MockActivity(DummyInjector):
        def get_object_graph(self):
            return mock_activity_obj_graph
    activity = MockActivity(mock_activity_obj_graph)
    fragment.get_modules = lambda: [InjectingFragmentModule(fragment, fragment)]
    mock_activity_obj_graph.plus = lambda *a: mock_fragment_obj_graph
    mock_fragment_obj_graph.inject = lambda target: None
    fragment.on_attach(activity)
    assert fragment.get_object_graph() == mock_fragment_obj_graph

def test_inject_graph_initialized():
    fragment = InjectingPreferenceFragment()
    mock_activity_obj_graph = DummyObjectGraph()
    mock_fragment_obj_graph = DummyObjectGraph()
    class MockActivity(DummyInjector):
        def get_object_graph(self):
            return mock_activity_obj_graph
    activity = MockActivity(mock_activity_obj_graph)
    fragment.get_modules = lambda: [InjectingFragmentModule(fragment, fragment)]
    mock_activity_obj_graph.plus = lambda *a: mock_fragment_obj_graph
    was_injected = {"called": False}
    def inject(target):
        was_injected["called"] = target
    mock_fragment_obj_graph.inject = inject
    fragment.on_attach(activity)
    target = object()
    fragment.inject(target)
    assert was_injected["called"] == target

def test_inject_graph_not_initialized():
    fragment = InjectingPreferenceFragment()
    with pytest.raises(IllegalStateException):
        fragment.inject(object())

def test_get_modules():
    fragment = InjectingPreferenceFragment()
    modules = fragment.get_modules()
    assert modules is not None
    assert len(modules) == 1
    assert isinstance(modules[0], InjectingFragmentModule)