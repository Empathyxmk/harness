package com.example.android.slidingtabsbasic;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import org.junit.*;
import org.robolectric.*;
import org.robolectric.annotation.Config;
import static org.mockito.Mockito.*;
import com.example.android.common.view.SlidingTabLayout;
import android.support.v4.view.ViewPager;

@Config(manifest=Config.NONE)
public class SlidingTabsBasicFragmentTest {

    @Test
    public void testOnCreateViewInflates() {
        SlidingTabsBasicFragment fragment = new SlidingTabsBasicFragment();
        LayoutInflater inflater = mock(LayoutInflater.class);
        ViewGroup container = mock(ViewGroup.class);
        Bundle bundle = new Bundle();
        View fakeView = mock(View.class);

        when(inflater.inflate(anyInt(), eq(container), eq(false))).thenReturn(fakeView);
        View v = fragment.onCreateView(inflater, container, bundle);
        Assert.assertEquals(fakeView, v);
    }

    @Test
    public void testOnViewCreated() {
        SlidingTabsBasicFragment fragment = new SlidingTabsBasicFragment();

        View view = mock(View.class);
        ViewPager pager = mock(ViewPager.class);
        SlidingTabLayout tabLayout = mock(SlidingTabLayout.class);

        when(view.findViewById(R.id.viewpager)).thenReturn(pager);
        when(view.findViewById(R.id.sliding_tabs)).thenReturn(tabLayout);

        fragment.onViewCreated(view, null);

        verify(pager).setAdapter(any(SlidingTabsBasicFragment.SamplePagerAdapter.class));
        verify(tabLayout).setViewPager(pager);
    }

    @Test
    public void testSamplePagerAdapterGetCountIsTen() {
        SlidingTabsBasicFragment fragment = new SlidingTabsBasicFragment();
        SlidingTabsBasicFragment.SamplePagerAdapter adapter = fragment.new SamplePagerAdapter();

        Assert.assertEquals(10, adapter.getCount());
    }

    @Test
    public void testIsViewFromObject() {
        SlidingTabsBasicFragment fragment = new SlidingTabsBasicFragment();
        SlidingTabsBasicFragment.SamplePagerAdapter adapter = fragment.new SamplePagerAdapter();

        View v = mock(View.class);
        // Same object, should return true
        Assert.assertTrue(adapter.isViewFromObject(v, v));
        // Different object, should return false
        Assert.assertFalse(adapter.isViewFromObject(mock(View.class), new Object()));
    }

    @Test
    public void testGetPageTitle() {
        SlidingTabsBasicFragment fragment = new SlidingTabsBasicFragment();
        SlidingTabsBasicFragment.SamplePagerAdapter adapter = fragment.new SamplePagerAdapter();

        for (int i = 0; i < adapter.getCount(); i++) {
            Assert.assertEquals("Item " + (i+1), adapter.getPageTitle(i));
        }
    }
}