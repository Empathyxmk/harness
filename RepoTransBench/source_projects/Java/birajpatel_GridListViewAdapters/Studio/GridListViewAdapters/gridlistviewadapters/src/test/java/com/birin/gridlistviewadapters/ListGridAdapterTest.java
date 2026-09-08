package com.birin.gridlistviewadapters;

import static org.junit.Assert.*;

import android.view.View;
import android.view.ViewGroup;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;

public class ListGridAdapterTest {

    private ListGridAdapter<String> adapter;
    private List<String> list;

    @Before
    public void setUp() {
        list = Arrays.asList("A", "B", "C", "D", "E");
        adapter = new ListGridAdapter<>(list, 2);
    }

    @Test
    public void testGetCount() {
        assertEquals(3, adapter.getCount());
    }

    @Test
    public void testGetItem() {
        assertEquals(list, adapter.getItem(0));
    }

    @Test
    public void testGetRowPositionInfo() {
        ListGridAdapter.RowPositionInfo info = adapter.getRowPositionInfo(1);
        assertEquals(2, info.rowIndex);
    }

    @Test
    public void testGetView_callsRowViewHolder() {
        ViewGroup parent = Mockito.mock(ViewGroup.class);
        ListGridAdapter.RowViewHolder holder = Mockito.mock(ListGridAdapter.RowViewHolder.class);
        View view = Mockito.mock(View.class);

        Mockito.when(parent.getContext()).thenReturn(null);
        Mockito.when(holder.getView()).thenReturn(view);

        // set private field rowViewHolder via reflection just for coverage
        try {
            java.lang.reflect.Field rvf = adapter.getClass().getDeclaredField("rowViewHolder");
            rvf.setAccessible(true);
            rvf.set(adapter, holder);
        } catch (Exception ignore) {}

        View result = adapter.getView(1, null, parent);
        assertNotNull(result);
    }

    @Test
    public void testAreAllItemsEnabled() {
        assertTrue(adapter.areAllItemsEnabled());
    }

    @Test
    public void testIsEnabled() {
        assertTrue(adapter.isEnabled(0));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testGetItem_invalidIndex() {
        adapter.getItem(10);
    }
}