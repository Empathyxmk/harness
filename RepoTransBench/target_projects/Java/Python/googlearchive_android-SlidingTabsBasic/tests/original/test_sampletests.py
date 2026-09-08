import pytest

class MainActivity:
    def __init__(self):
        self.fragments = [object(), SlidingTabsBasicFragment()]

    def getSupportFragmentManager(self):
        return self

    def getFragments(self):
        return self.fragments

class SlidingTabsBasicFragment:
    pass

@pytest.fixture
def mTestActivity():
    return MainActivity()

@pytest.fixture
def mTestFragment(mTestActivity):
    return mTestActivity.getFragments()[1]

def test_preconditions(mTestActivity, mTestFragment):
    assert mTestActivity is not None, "mTestActivity is null"
    assert mTestFragment is not None, "mTestFragment is null"