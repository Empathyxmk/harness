import pytest
from unittest.mock import MagicMock

class MapActivity:
    def __init__(self):
        class ViewPager_PageTransformer:
            pass
        class ViewPager_OnPageChangeListener:
            def on_page_scroll_state_changed(self, state): pass
            def on_page_selected(self, pos): pass
            def on_page_scrolled(self, pos, offset, px): pass
        self.pageTransformer = ViewPager_PageTransformer()
        self.pageChangeListener = ViewPager_OnPageChangeListener()
        self.created = False

    def on_create(self, bundle):
        self.created = True

@pytest.fixture
def activity():
    return MapActivity()

def test_on_create_executes_without_crash(activity):
    activity.on_create({})
    assert activity.created

def test_page_transformer_no_crash(activity):
    assert activity.pageTransformer is not None

def test_page_change_listener_no_crash(activity):
    plc = activity.pageChangeListener
    plc.on_page_scroll_state_changed(0)
    plc.on_page_selected(0)
    plc.on_page_scrolled(0, 0.5, 20)
    assert plc is not None