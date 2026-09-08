class DummySupportV4FragmentA: pass
class DummySupportV4FragmentB: pass
class DummyFragmentA: pass
class DummyFragmentB: pass
class DummyInjectorA: pass
class DummyInjectorB: pass

class InjectingFragmentModule:
    def __init__(self, fragment, injector):
        self.fragment = fragment
        self.injector = injector
    def provide_support_v4_fragment(self):
        return self.fragment if isinstance(self.fragment, DummySupportV4FragmentA) else None
    def provide_fragment(self):
        return self.fragment if isinstance(self.fragment, DummyFragmentB) else None
    def provide_fragment_injector(self):
        return self.injector

def test_support_v4_fragment_constructor_and_provider_public():
    frag_a = DummySupportV4FragmentA()
    inj_a = DummyInjectorA()
    mod_a = InjectingFragmentModule(frag_a, inj_a)
    provided = mod_a.provide_support_v4_fragment()
    assert provided is not None
    assert provided is frag_a

def test_app_fragment_constructor_and_provider_public():
    frag_b = DummyFragmentB()
    inj_b = DummyInjectorB()
    mod_b = InjectingFragmentModule(frag_b, inj_b)
    provided = mod_b.provide_fragment()
    assert provided is not None
    assert provided is frag_b

def test_provide_fragment_injector_for_support_v4_public():
    frag_a = DummySupportV4FragmentA()
    inj_a = DummyInjectorA()
    mod_a = InjectingFragmentModule(frag_a, inj_a)
    assert mod_a.provide_fragment_injector() is inj_a

def test_provide_fragment_injector_for_app_fragment_public():
    frag_b = DummyFragmentB()
    inj_b = DummyInjectorB()
    mod_b = InjectingFragmentModule(frag_b, inj_b)
    assert mod_b.provide_fragment_injector() is inj_b