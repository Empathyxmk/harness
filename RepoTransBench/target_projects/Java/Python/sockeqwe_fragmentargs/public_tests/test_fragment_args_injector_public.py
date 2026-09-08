from tests.original.test_fragment_args import FragmentArgsInjector

def test_injector_interface_should_allow_any_object_public_test():
    class DummyPublicInjector(FragmentArgsInjector):
        def inject(self, target):
            if isinstance(target, float):
                pass  # accept float
    inj = DummyPublicInjector()
    inj.inject(77.7)