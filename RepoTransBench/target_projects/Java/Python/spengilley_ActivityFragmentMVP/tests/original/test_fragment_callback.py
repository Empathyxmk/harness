import pytest

class FragmentCallback:
    def load_detail_fragment(self):
        raise NotImplementedError

    def finish_process(self):
        raise NotImplementedError

def test_interface():
    # cover the interface by implementing it
    class CB(FragmentCallback):
        def load_detail_fragment(self):
            pass
        def finish_process(self):
            pass

    cb = CB()
    cb.load_detail_fragment()
    cb.finish_process()