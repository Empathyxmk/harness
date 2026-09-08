package com.github.markzhai.recyclerview;

import android.content.Context;
import android.view.LayoutInflater;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.Assert.*;

public class MultiTypeAdapterPublicTest {

    private Context context;
    private LayoutInflater inflater;

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
    }

    @Test
    public void testAddAndViewTypePublic() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(9, 109);
        adapter.add("baz", 9);
        assertEquals(1, adapter.getItemCount());
        assertEquals(9, adapter.getItemViewType(0));
    }

    @Test
    public void testAddAllAndSetPublic() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(11, 111);

        List<String> list = Arrays.asList("p", "q", "r");
        adapter.addAll(list, 11);
        assertEquals(3, adapter.getItemCount());
        assertEquals(11, adapter.getItemViewType(2));
        adapter.set(Arrays.asList("v", "w", "z"), 11);
        assertEquals(3, adapter.getItemCount());
        assertEquals(11, adapter.getItemViewType(0));
    }

    @Test
    public void testRemoveClearPublic() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(7, 107);
        adapter.add("car", 7);
        assertEquals(1, adapter.getItemCount());
        adapter.remove(0);
        assertEquals(0, adapter.getItemCount());
        adapter.add("bus", 7);
        adapter.clear();
        assertEquals(0, adapter.getItemCount());
    }

    @Test
    public void testSetWithTyperPublic() {
        MultiTypeAdapter.MultiViewTyper typer = Mockito.mock(MultiTypeAdapter.MultiViewTyper.class);
        Mockito.when(typer.getViewType(Mockito.any())).thenReturn(4);
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(4, 104);
        adapter.set(Arrays.asList("k", "l", "m"), typer);
        assertEquals(3, adapter.getItemCount());
        assertEquals(4, adapter.getItemViewType(2));
    }

    @Test
    public void testAddAtPositionAndAddAllPositionPublic() {
        MultiTypeAdapter adapter = new MultiTypeAdapter(context);
        adapter.addViewTypeToLayoutMap(15, 115);

        adapter.add("apple", 15);
        adapter.add(0, "banana", 15);

        List<String> list = Arrays.asList("pear", "peach");
        adapter.addAll(0, list, 15);
        assertEquals(4, adapter.getItemCount());
        assertEquals(15, adapter.getItemViewType(3));
    }
}