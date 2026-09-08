class DummyActivity:
    pass
class DummyInjector:
    pass

class InjectingActivityModule:
    def __init__(self, activity, injector):
        self._activity = activity
        self._injector = injector
    def provide_activity_context(self):
        return self._activity
    def provide_activity(self):
        return self._activity
    def provide_activity_injector(self):
        return self._injector

def test_provide_activity_context():
    activity = DummyActivity()
    injector = DummyInjector()
    module = InjectingActivityModule(activity, injector)
    ctx = module.provide_activity_context()
    assert ctx is not None
    assert ctx == activity

def test_provide_activity():
    activity = DummyActivity()
    injector = DummyInjector()
    module = InjectingActivityModule(activity, injector)
    act = module.provide_activity()
    assert act is not None
    assert act == activity

def test_provide_activity_injector():
    activity = DummyActivity()
    injector = DummyInjector()
    module = InjectingActivityModule(activity, injector)
    inj = module.provide_activity_injector()
    assert inj is not None
    assert inj == injector