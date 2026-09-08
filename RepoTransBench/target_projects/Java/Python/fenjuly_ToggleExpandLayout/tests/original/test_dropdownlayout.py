import pytest
from unittest.mock import Mock

# Dummy stand-ins for library classes.
class DummyToggleExpandLayout:
    def __init__(self):
        self.was_layouted = False

    def on_layout(self):
        self.was_layouted = True

class DummyDropDownLayout:
    def __init__(self, child):
        self.child = child
        self.layout_called = False
        self.child_layouted = False

    def get_child_count(self):
        return 1

    def get_child_at(self, idx):
        if idx == 0:
            return self.child
        return None

    def on_layout(self):
        self.layout_called = True
        child = self.get_child_at(0)
        # Only call on_layout if the child is a ToggleExpandLayout
        if hasattr(child, "on_layout") and isinstance(child, DummyToggleExpandLayout):
            child.on_layout()
            self.child_layouted = child.was_layouted

def test_on_layout_with_simple_child():
    # Simulate 1 child, which is NOT a ToggleExpandLayout (Mock instead)
    normal_child = Mock()
    layout = DummyDropDownLayout(normal_child)
    layout.on_layout()
    assert layout.layout_called is True
    # Child should NOT be called with on_layout, since it's not a DummyToggleExpandLayout
    assert not getattr(layout, "child_layouted", False)

def test_on_layout_with_toggle_expand_layout_child():
    # Simulate 1 child, which IS a DummyToggleExpandLayout
    toggle_child = DummyToggleExpandLayout()
    layout = DummyDropDownLayout(toggle_child)
    layout.on_layout()
    assert layout.layout_called is True
    # Now the child's on_layout should be called, and it should be tracked
    assert layout.child_layouted is True
    assert toggle_child.was_layouted is True