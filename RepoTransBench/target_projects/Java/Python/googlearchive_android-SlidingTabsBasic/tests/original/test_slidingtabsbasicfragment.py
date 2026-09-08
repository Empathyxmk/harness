import pytest
from unittest.mock import Mock, MagicMock, call, ANY
import types

class SlidingTabsBasicFragment:
    class SamplePagerAdapter:
        def getCount(self):
            return 10

        def isViewFromObject(self, view, obj):
            return view is obj

        def getPageTitle(self, position):
            return f"Item {position + 1}"

    def onCreateView(self, inflater, container, bundle):
        # Simulate Java behavior: delegated inflation
        return inflater.inflate(ANY, container, False)

    def onViewCreated(self, view, unused):
        pager = view.findViewById('viewpager')
        tabLayout = view.findViewById('sliding_tabs')
        if pager:
            pager.setAdapter(self.SamplePagerAdapter())
        if tabLayout:
            tabLayout.setViewPager(pager)

@pytest.fixture
def fragment():
    return SlidingTabsBasicFragment()

def test_on_create_view_inflates(fragment):
    inflater = Mock()
    container = object()
    bundle = object()
    fake_view = object()
    inflater.inflate.return_value = fake_view

    v = fragment.onCreateView(inflater, container, bundle)
    assert v == fake_view

def test_on_view_created(fragment):
    view = Mock()
    pager = Mock()
    tabLayout = Mock()
    view.findViewById = Mock(side_effect=lambda x: { 'viewpager': pager, 'sliding_tabs': tabLayout }[x])

    fragment.onViewCreated(view, None)
    assert pager.setAdapter.called
    assert tabLayout.setViewPager.called
    # Optionally, check call arguments

def test_sample_pager_adapter_get_count_is_ten(fragment):
    adapter = fragment.SamplePagerAdapter()
    assert adapter.getCount() == 10

def test_is_view_from_object(fragment):
    adapter = fragment.SamplePagerAdapter()
    v = object()
    assert adapter.isViewFromObject(v, v)
    assert not adapter.isViewFromObject(object(), object())

def test_get_page_title(fragment):
    adapter = fragment.SamplePagerAdapter()
    for i in range(adapter.getCount()):
        assert adapter.getPageTitle(i) == f"Item {i+1}"