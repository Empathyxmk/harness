import pytest

class FileChooseInterceptor:
    def on_file_chosen(self, context, sel, orig, code, action):
        raise NotImplementedError

    def describe_contents(self):
        raise NotImplementedError

    def write_to_parcel(self, dest, flags):
        raise NotImplementedError

class DummyImpl(FileChooseInterceptor):
    def on_file_chosen(self, context, sel, orig, code, action):
        return sel is not None and len(sel) > 0 and orig and code == 2 and action is None

    def describe_contents(self):
        return 0

    def write_to_parcel(self, dest, flags):
        pass

    @classmethod
    def creator_new_array(cls, size):
        return [DummyImpl() for _ in range(size)]

    @classmethod
    def creator_create_from_parcel(cls, source):
        return DummyImpl()

def test_on_file_chosen():
    impl = DummyImpl()
    sel = ["pic1"]
    assert impl.on_file_chosen(None, sel, True, 2, None)

def test_parcelable():
    impl = DummyImpl()
    assert impl.describe_contents() == 0
    impl.write_to_parcel(None, 0)
    arr = DummyImpl.creator_new_array(3)
    assert len(arr) == 3
    inst = DummyImpl.creator_create_from_parcel(None)
    assert inst is not None