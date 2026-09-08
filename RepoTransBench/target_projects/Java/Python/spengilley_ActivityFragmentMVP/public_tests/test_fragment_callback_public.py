import pytest

class FragmentCallback:
    def on_action(self, s):
        raise NotImplementedError

def test_dummy_test_for_callback():
    # As FragmentCallback is an interface, let's test instantiation w/ different lambda/body
    class Callback(FragmentCallback):
        def on_action(self, s):
            # Public test: act on a different string than original test
            assert s == "PublicAction"

    callback = Callback()
    callback.on_action("PublicAction")