import pytest
from unittest.mock import Mock, ANY, call

class SlidingTabsBasicFragment:
    class SamplePagerAdapter:
        def getCount(self):
            return 11

        def isViewFromObject(self, view, obj):
            return view is obj

        def getPageTitle(self, position):
            return f"Tab {position * 2}"

    def onCreateView(self, inflater, container, bundle):
        # simulate "publicFakeView" situation
        return inflater.inflate(123456, container, False)

    def onViewCreated(self, view, unused):
        pager = view.findViewById(777)
        tab_layout = view.findViewById(888)
        if pager:
            pager.setAdapter(SlidingTabsBasicFragment.SamplePagerAdapter())
        if tab_layout:
            tab_layout.setViewPager(pager)

def test_on_create_view_inflates_different_view():
    fragment = SlidingTabsBasicFragment()
    inflater = Mock()
    container = object()
    bundle = object()
    fake_view = object()
    inflater.inflate.return_value = fake_view

    # Should call with uniqueResId
    v = fragment.onCreateView(inflater, container, bundle)
    assert v == fake_view

def test_on_view_created_with_different_mocks():
    fragment = SlidingTabsBasicFragment()
    view = Mock()
    pager = Mock()
    tabLayout = Mock()
    view.findViewById = Mock(side_effect=lambda x: {777: pager, 888: tabLayout}[x])

    fragment.onViewCreated(view, None)
    assert pager.setAdapter.called
    assert tabLayout.setViewPager.called

def test_sample_pager_adapter_get_count_is_eleven_public():
    fragment = SlidingTabsBasicFragment()
    adapter = fragment.SamplePagerAdapter()
    assert adapter.getCount() == 11

def test_is_view_from_object_different_objects():
    fragment = SlidingTabsBasicFragment()
    adapter = fragment.SamplePagerAdapter()
    v1 = object()
    v2 = object()
    assert not adapter.isViewFromObject(v1, v2)
    assert adapter.isViewFromObject(v2, v2)

def test_get_page_title_public():
    fragment = SlidingTabsBasicFragment()
    adapter = SlidingTabsBasicFragment.SamplePagerAdapter()
    for i in range(adapter.getCount()):
        assert adapter.getPageTitle(i) == f"Tab {i * 2}"