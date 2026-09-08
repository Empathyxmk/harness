from tests.original.test_fragment_args import FragmentArgsInjector

def test_injector_interface_should_allow_any_object():
    class DummyInjector(FragmentArgsInjector):
        def inject(self, target):
            # no-op
            pass

    inj = DummyInjector()
    inj.inject("dummy")