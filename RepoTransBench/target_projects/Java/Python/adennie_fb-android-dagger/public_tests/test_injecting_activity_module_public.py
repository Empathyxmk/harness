class DummyActivity1: pass
class DummyActivity2: pass
class DummyInjector1: pass
class DummyInjector2: pass

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

def test_provide_activity_context_public():
    activity1 = DummyActivity1()
    injector1 = DummyInjector1()
    activity2 = DummyActivity2()
    injector2 = DummyInjector2()
    module1 = InjectingActivityModule(activity1, injector1)
    module2 = InjectingActivityModule(activity2, injector2)
    ctx1 = module1.provide_activity_context()
    ctx2 = module2.provide_activity_context()
    assert ctx1 is not None and ctx1 == activity1
    assert ctx2 is not None and ctx2 == activity2

def test_provide_activity_public():
    activity1 = DummyActivity1()
    injector1 = DummyInjector1()
    activity2 = DummyActivity2()
    injector2 = DummyInjector2()
    module1 = InjectingActivityModule(activity1, injector1)
    module2 = InjectingActivityModule(activity2, injector2)
    assert module1.provide_activity() == activity1
    assert module2.provide_activity() == activity2

def test_provide_activity_injector_public():
    activity1 = DummyActivity1()
    injector1 = DummyInjector1()
    activity2 = DummyActivity2()
    injector2 = DummyInjector2()
    module1 = InjectingActivityModule(activity1, injector1)
    module2 = InjectingActivityModule(activity2, injector2)
    assert module1.provide_activity_injector() == injector1
    assert module2.provide_activity_injector() == injector2