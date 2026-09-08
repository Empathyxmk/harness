import pytest
from unittest.mock import Mock

class DummyDropDownLayout:
    def __init__(self, context):
        self.context = context

    def getChildCount(self):
        return 0

    def getChildAt(self, i):
        raise IndexError

    def onLayout(self, changed, l, t, r, b):
        for i in range(self.getChildCount()):
            child = self.getChildAt(i)
            child.getMeasuredWidth()
            child.getMeasuredHeight()
            if isinstance(child, DummyToggleExpandLayout):
                for j in range(child.getChildCount()):
                    grandchild = child.getChildAt(j)
                    grandchild.getMeasuredWidth()
                    grandchild.getMeasuredHeight()

class DummyToggleExpandLayout:
    def __init__(self):
        pass
    def getChildCount(self): return 0
    def getChildAt(self, i): raise IndexError

def test_on_layout_with_different_simple_child(mocker):
    # 2 children, both not ToggleExpandLayout
    layout = mocker.spy(DummyDropDownLayout(Mock()))
    child1 = Mock()
    child2 = Mock()
    mocker.patch.object(layout, "getChildCount", return_value=2)
    mocker.patch.object(layout, "getChildAt", side_effect=[child1, child2])
    child1.getMeasuredWidth.return_value = 13
    child1.getMeasuredHeight.return_value = 8
    child2.getMeasuredWidth.return_value = 17
    child2.getMeasuredHeight.return_value = 4
    layout.onLayout(True, 2, 3, 7, 12)  # Should not rush/raise

def test_on_layout_with_different_toggle_expand_layout_child(mocker):
    layout = mocker.spy(DummyDropDownLayout(Mock()))
    toggle_child = mocker.create_autospec(DummyToggleExpandLayout)
    grand_child1 = Mock()
    grand_child2 = Mock()
    child2 = Mock()

    mocker.patch.object(layout, "getChildCount", return_value=2)
    mocker.patch.object(layout, "getChildAt", side_effect=[toggle_child, child2])

    toggle_child.getMeasuredWidth.return_value = 30
    toggle_child.getMeasuredHeight.return_value = 6
    toggle_child.getChildCount.return_value = 2
    toggle_child.getChildAt.side_effect = [grand_child1, grand_child2]
    grand_child1.getMeasuredWidth.return_value = 20
    grand_child1.getMeasuredHeight.return_value = 5
    grand_child2.getMeasuredWidth.return_value = 9
    grand_child2.getMeasuredHeight.return_value = 2

    child2.getMeasuredWidth.return_value = 14
    child2.getMeasuredHeight.return_value = 7

    layout.onLayout(False, 4, 5, 6, 10)  # Should not raise