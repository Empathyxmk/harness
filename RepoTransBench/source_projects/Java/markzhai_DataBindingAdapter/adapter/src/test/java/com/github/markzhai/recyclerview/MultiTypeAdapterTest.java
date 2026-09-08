package com.github.markzhai.recyclerview;

import android.content.Context;
import android.view.LayoutInflater;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.Assert.*;

public class MultiTypeAdapterTest {

    private Context context;
    private LayoutInflater inflater;

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
    }

    @Test
    public void testAddAndViewType() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(1, 100);
        adapter.add("foo", 1);
        assertEquals(1, adapter.getItemCount());
        assertEquals(1, adapter.getItemViewType(0));
    }

    @Test
    public void testAddAllAndSet() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(8, 108);

        List<String> list = Arrays.asList("a", "b");
        adapter.addAll(list, 8);
        assertEquals(2, adapter.getItemCount());
        assertEquals(8, adapter.getItemViewType(1));
        adapter.set(Arrays.asList("x", "y"), 8);
        assertEquals(2, adapter.getItemCount());
        assertEquals(8, adapter.getItemViewType(0));
    }

    @Test
    public void testRemoveClear() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(2, 102);
        adapter.add("bar", 2);
        assertEquals(1, adapter.getItemCount());
        adapter.remove(0);
        assertEquals(0, adapter.getItemCount());
        adapter.add("foo", 2);
        adapter.clear();
        assertEquals(0, adapter.getItemCount());
    }

    @Test
    public void testSetWithTyper() {
        MultiTypeAdapter.MultiViewTyper typer = Mockito.mock(MultiTypeAdapter.MultiViewTyper.class);
        Mockito.when(typer.getViewType(Mockito.any())).thenReturn(3);
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(3, 103);
        adapter.set(Arrays.asList("f", "g"), typer);
        assertEquals(2, adapter.getItemCount());
        assertEquals(3, adapter.getItemViewType(1));
    }

    @Test
    public void testAddAtPositionAndAddAllPosition() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(5, 105);

        adapter.add("m", 5);
        adapter.add(0, "n", 5);

        List<String> list = Arrays.asList("a", "b");
        adapter.addAll(0, list, 5);
        assertEquals(4, adapter.getItemCount());
        assertEquals(5, adapter.getItemViewType(2));
    }
}