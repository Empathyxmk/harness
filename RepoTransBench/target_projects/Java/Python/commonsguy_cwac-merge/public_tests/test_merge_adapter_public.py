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

def test_single_adapter_different_data():
    # Use different data from original test
    dummy = DummyAdapter([42, 7, 18])
    merge = MergeAdapter(dummy)

    assert merge.get_count() == 3, "Count should equal original size"
    assert merge.get_item(0) == 42, "First item should be 42"
    assert merge.get_item(1) == 7, "Second item should be 7"
    assert merge.get_item(2) == 18, "Third item should be 18"

def test_multiple_adapters_different_data():
    # Different integers from the existing (original) test
    dummy_a = DummyAdapter([91, 22])
    dummy_b = DummyAdapter([55, 66])
    merge = MergeAdapter()
    merge.add_adapter(dummy_a)
    merge.add_adapter(dummy_b)

    assert merge.get_count() == 4, "Count should be sum of counts"
    assert merge.get_item(0) == 91
    assert merge.get_item(1) == 22
    assert merge.get_item(2) == 55
    assert merge.get_item(3) == 66