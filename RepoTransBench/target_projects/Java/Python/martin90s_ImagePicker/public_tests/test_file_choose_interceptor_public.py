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
        return sel is not None and len(sel) > 1 and not orig and code == 5 and action is not None

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

class PickerAction:
    pass

def test_on_file_chosen_with_different_data():
    impl = DummyImpl()
    sel = ["picA", "picB"]
    assert impl.on_file_chosen(None, sel, False, 5, PickerAction())

def test_parcelable_different_size():
    impl = DummyImpl()
    assert impl.describe_contents() == 0
    impl.write_to_parcel(None, 0)
    arr = DummyImpl.creator_new_array(2)
    assert len(arr) == 2
    inst = DummyImpl.creator_create_from_parcel(None)
    assert inst is not None