from unittest.mock import MagicMock

class CarsPagerAdapter:
    def __init__(self, items):
        self.items = items

    def get_count(self):
        return len(self.items)

    def is_view_from_object(self, view, obj):
        return view is obj

    def instantiate_item(self, container, position):
        pass

    def destroy_item(self, container, position, obj):
        pass

def test_get_count_returns_list_size_public():
    adapter = CarsPagerAdapter([2,3,2])
    assert adapter.get_count() == 3

def test_is_view_from_object_returns_true_if_same_public():
    view = object()
    adapter = CarsPagerAdapter([2,3,2])
    assert adapter.is_view_from_object(view, view)

def test_instantiate_and_destroy_item_no_crash_public():
    adapter = CarsPagerAdapter([2,3,2])
    container = MagicMock()
    adapter.instantiate_item(container, 1)
    adapter.destroy_item(container, 2, object())