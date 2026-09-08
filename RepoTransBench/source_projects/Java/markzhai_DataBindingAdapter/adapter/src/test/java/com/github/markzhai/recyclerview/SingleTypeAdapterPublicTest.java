package com.github.markzhai.recyclerview;

import android.content.Context;
import android.view.LayoutInflater;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.*;

import static org.junit.Assert.*;

public class SingleTypeAdapterPublicTest {

    private Context context;
    private LayoutInflater inflater;

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
    }

    @Test
    public void testAddAndCountPublic() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 1222);
        adapter.add("delta");
        assertEquals(1, adapter.getItemCount());
        assertEquals(1222, adapter.getLayoutRes());
    }

    @Test
    public void testAddAtPositionPublic() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 2121);
        adapter.add("sigma");
        adapter.add(0, "theta");
        assertEquals(2, adapter.getItemCount());
        // First item is "theta"
        assertEquals("theta", adapter.mCollection.get(0));
        assertEquals("sigma", adapter.mCollection.get(1));
    }

    @Test
    public void testSetPublic() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 3333);
        List<String> items = Arrays.asList("alpha", "beta", "gamma");
        adapter.set(items);
        assertEquals(3, adapter.getItemCount());
        assertEquals("alpha", adapter.mCollection.get(0));
        assertEquals("gamma", adapter.mCollection.get(2));
    }

    @Test
    public void testAddAllPublic() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 4343);
        List<String> items = Arrays.asList("one", "two");
        adapter.addAll(items);
        assertEquals(2, adapter.getItemCount());
        adapter.add("three");
        assertEquals(3, adapter.getItemCount());
    }
}