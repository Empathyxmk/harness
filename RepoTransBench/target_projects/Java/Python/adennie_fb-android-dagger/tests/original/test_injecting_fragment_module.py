from unittest import mock

class DummyV4Fragment: pass
class DummyAppFragment: pass
class DummyInjector: pass

class InjectingFragmentModule:
    def __init__(self, fragment, injector):
        self.fragment = fragment
        self.injector = injector
    def provide_support_v4_fragment(self):
        return self.fragment if isinstance(self.fragment, DummyV4Fragment) else None
    def provide_fragment(self):
        return self.fragment if not isinstance(self.fragment, DummyV4Fragment) else None
    def provide_fragment_injector(self):
        return self.injector

def test_support_v4_fragment_constructor_and_provider():
    v4frag = DummyV4Fragment()
    injector = DummyInjector()
    mod = InjectingFragmentModule(v4frag, injector)
    provided = mod.provide_support_v4_fragment()
    assert provided is not None
    assert provided is v4frag

def test_app_fragment_constructor_and_provider():
    appfrag = DummyAppFragment()
    injector = DummyInjector()
    mod = InjectingFragmentModule(appfrag, injector)
    provided = mod.provide_fragment()
    assert provided is not None
    assert provided is appfrag

def test_provide_fragment_injector_for_support_v4():
    v4frag = DummyV4Fragment()
    injector = DummyInjector()
    mod = InjectingFragmentModule(v4frag, injector)
    assert mod.provide_fragment_injector() is injector

def test_provide_fragment_injector_for_app_fragment():
    appfrag = DummyAppFragment()
    injector = DummyInjector()
    mod = InjectingFragmentModule(appfrag, injector)
    assert mod.provide_fragment_injector() is injector