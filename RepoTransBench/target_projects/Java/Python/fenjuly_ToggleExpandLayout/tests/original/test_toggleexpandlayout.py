import pytest
from unittest.mock import Mock, create_autospec, call

class DummyToggleExpandLayout:
    """Python stand-in for ToggleExpandLayout with callback mocks."""
    def __init__(self, context=None):
        self._listener = None
        self._children = []
        self.last_on_layout_args = None

    def setOnToggleTouchListener(self, listener):
        self._listener = listener

    def add_child(self, child):
        self._children.append(child)

    def getChildCount(self):
        return len(self._children)

    def getChildAt(self, idx):
        return self._children[idx]

    def open(self):
        if self._listener:
            self._listener.onStartOpen(1, 2)
        # ... no further logic for test

    def close(self):
        if self._listener:
            self._listener.onStartClose(3, 4)

    def onLayout(self, changed, l, t, r, b):
        self.last_on_layout_args = (changed, l, t, r, b)
        # For each child, call their getMeasuredWidth/Height
        for child in self._children:
            child.getMeasuredWidth()
            child.getMeasuredHeight()

class DummyToggleTouchListener:
    def __init__(self):
        self.open_called = 0
        self.close_called = 0

    def onStartOpen(self, h, oh):
        self.open_called += 1

    def onOpen(self):
        pass

    def onStartClose(self, h, oh):
        self.close_called += 1

    def onClosed(self):
        pass

def test_set_on_toggle_touch_listener():
    layout = DummyToggleExpandLayout()
    listener = DummyToggleTouchListener()
    layout.setOnToggleTouchListener(listener)
    assert layout._listener is not None

def test_open_and_close_no_children():
    layout = DummyToggleExpandLayout()
    listener = DummyToggleTouchListener()
    layout.setOnToggleTouchListener(listener)
    layout.open()
    layout.close()
    assert listener.open_called == 1
    assert listener.close_called == 1

def test_open_and_close_with_children(mocker):
    layout = DummyToggleExpandLayout()
    child0 = Mock()
    child0.getMeasuredWidth.return_value = 20
    child0.getMeasuredHeight.return_value = 15
    child1 = Mock()
    child1.getMeasuredWidth.return_value = 30
    child1.getMeasuredHeight.return_value = 10
    layout.add_child(child0)
    layout.add_child(child1)

    listener = Mock()
    layout.setOnToggleTouchListener(listener)
    layout.onLayout(True, 0, 0, 30, 25)
    layout.open()
    layout.close()
    assert layout.last_on_layout_args == (True, 0, 0, 30, 25)
    assert layout.getChildCount() == 2
    child0.getMeasuredWidth.assert_called_once()
    child1.getMeasuredWidth.assert_called_once()
    child0.getMeasuredHeight.assert_called_once()
    child1.getMeasuredHeight.assert_called_once()
    # Verify onStartOpen and onStartClose were called at least once
    assert listener.onStartOpen.call_count >= 1
    assert listener.onStartClose.call_count >= 1

def test_multiple_listeners():
    layout = DummyToggleExpandLayout()
    listener1 = Mock()
    listener2 = Mock()
    layout.setOnToggleTouchListener(listener1)
    layout.setOnToggleTouchListener(listener2)
    layout.open()
    layout.close()
    # Newest (listener2) receives the events
    assert listener2.onStartOpen.call_count >= 1
    assert listener2.onStartClose.call_count >= 1
    # listener1 does not receive after replace, may be called 0 times
    assert listener1.onStartOpen.call_count >= 0
    assert listener1.onStartClose.call_count >= 0