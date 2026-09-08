package com.github.markzhai.recyclerview;

import android.content.Context;
import android.view.LayoutInflater;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class SingleTypeAdapterTest {

    private Context context;
    private LayoutInflater inflater;

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
    }

    @Test
    public void testConstructorAndGetters() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 123);
        assertEquals(0, adapter.getItemCount());
        assertEquals(123, adapter.getLayoutRes());
    }

    @Test
    public void testAdd() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 321);
        adapter.add("foo");
        assertEquals(1, adapter.getItemCount());
    }

    @Test
    public void testAddAtPosition() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 321);
        adapter.add("foo");
        adapter.add(0, "bar");
        assertEquals(2, adapter.getItemCount());
    }

    @Test
    public void testSetAndAddAll() {
        SingleTypeAdapter<String> adapter = new SingleTypeAdapter<>(context, 321);
        adapter.set(Arrays.asList("a", "b"));
        assertEquals(2, adapter.getItemCount());
        adapter.addAll(Collections.singletonList("c"));
        assertEquals(3, adapter.getItemCount());
    }
}