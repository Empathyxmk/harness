import pytest

class DummyAdapter:
    def __init__(self, data):
        self.data = list(data)

    def are_all_items_enabled(self):
        return True

    def is_enabled(self, position):
        return True

    def register_data_set_observer(self, observer):
        pass

    def unregister_data_set_observer(self, observer):
        pass

    def get_count(self):
        return len(self.data)

    def get_item(self, position):
        return self.data[position]

    def get_item_id(self, position):
        return position

    def has_stable_ids(self):
        return False

    def get_view(self, position, convert_view, parent):
        return None

    def get_item_view_type(self, position):
        return 0

    def get_view_type_count(self):
        return 1

    def is_empty(self):
        return len(self.data) == 0

class MergeAdapter:
    def __init__(self, *adapters):
        self.adapter_list = list(adapters)

    def add_adapter(self, adapter):
        self.adapter_list.append(adapter)

    def get_count(self):
        return sum(a.get_count() for a in self.adapter_list)

    def get_item(self, pos):
        offset = 0
        for a in self.adapter_list:
            count = a.get_count()
            if pos < offset + count:
                return a.get_item(pos - offset)
            offset += count
        return None

def test_single_adapter():
    dummy = DummyAdapter([1, 2, 3])
    merge = MergeAdapter(dummy)

    assert merge.get_count() == 3, "Count should equal original size"
    assert merge.get_item(0) == 1, "First item should be 1"
    assert merge.get_item(1) == 2, "Second item should be 2"
    assert merge.get_item(2) == 3, "Third item should be 3"

def test_multiple_adapters():
    dummy = DummyAdapter([10, 20])
    dummy2 = DummyAdapter([30])
    merge = MergeAdapter()
    merge.add_adapter(dummy)
    merge.add_adapter(dummy2)

    assert merge.get_count() == 3, "Count should be sum of counts"
    assert merge.get_item(0) == 10
    assert merge.get_item(1) == 20
    assert merge.get_item(2) == 30