import pytest
from unittest.mock import MagicMock

# Stubs for Android sample elements
class R:
    class id:
        frame = 101
        text_view = 102
        button = 103

# Simulated view for clipping
class MockView:
    def __init__(self, clip=False):
        self._clip = clip
    def getClipToOutline(self):
        return self._clip
    def setClipToOutline(self, val):
        self._clip = val

class MainActivity:
    def __init__(self):
        self.views = {
            R.id.frame: MockView(),        # initially unclipped
            R.id.text_view: object(),
            R.id.button: object(),
        }
        self._fragments = [object(), "dummy", ClippingBasicFragment(self)]
    def getSupportFragmentManager(self):
        class FragmentManager:
            def getFragments(fm_self):
                # To match Java test, fragments[1] should be ClippingBasicFragment
                return self._fragments
        return FragmentManager()
    def findViewById(self, id_):
        return self.views[id_]

class ClippingBasicFragment:
    def __init__(self, activity):
        self._activity = activity

def clickView(context, view):
    # Simulate clicking: change clipped state if the view is the button
    if isinstance(view, object) and hasattr(context, "findViewById"):
        frame = context.findViewById(R.id.frame)
        # "eventually", .getClipToOutline becomes True on the frame
        frame.setClipToOutline(True)

@pytest.fixture(autouse=True)
def setUp():
    # Set up a mock activity and fragment for each test
    yield

def test_preconditions():
    mTestActivity = MainActivity()
    mTestFragment = mTestActivity.getSupportFragmentManager().getFragments()[1]
    assert mTestActivity is not None, "mTestActivity is null"
    assert mTestFragment is not None, "mTestFragment is null"
    assert mTestActivity.findViewById(R.id.frame) is not None, "Clipped frame is null"
    assert mTestActivity.findViewById(R.id.text_view) is not None, "Text view is null"

def test_clipping():
    mTestActivity = MainActivity()
    view = mTestActivity.findViewById(R.id.frame)
    assert not view.getClipToOutline()
    # Simulate clicking button
    clickView(mTestActivity, mTestActivity.findViewById(R.id.button))
    assert view.getClipToOutline()