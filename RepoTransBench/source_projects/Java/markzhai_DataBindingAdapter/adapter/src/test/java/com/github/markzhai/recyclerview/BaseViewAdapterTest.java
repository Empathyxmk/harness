package com.github.markzhai.recyclerview;

import android.content.Context;
import android.view.LayoutInflater;

import com.github.markzhai.recyclerview.BaseViewAdapter.Decorator;
import com.github.markzhai.recyclerview.BaseViewAdapter.Presenter;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;

import static org.junit.Assert.*;

public class BaseViewAdapterTest {

    class TestAdapter extends BaseViewAdapter<String> {
        TestAdapter(Context c) { super(c); mCollection = new java.util.ArrayList<>(); }
        @Override public BindingViewHolder onCreateViewHolder(android.view.ViewGroup parent, int viewType) { return null; }
        @Override public void onBindViewHolder(BindingViewHolder holder, int position) {}
    }

    private TestAdapter adapter;
    private Context context;
    private LayoutInflater inflater;

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
        adapter = new TestAdapter(context);
        adapter.mCollection.addAll(Arrays.asList("a", "b", "c"));
    }

    @Test
    public void testRemove() {
        adapter.remove(1);
        assertEquals(2, adapter.getItemCount());
        assertEquals("a", adapter.mCollection.get(0));
        assertEquals("c", adapter.mCollection.get(1));
    }

    @Test
    public void testClear() {
        adapter.clear();
        assertEquals(0, adapter.getItemCount());
    }

    @Test
    public void testSetPresenterAndDecorator() {
        Presenter p = Mockito.mock(Presenter.class);
        adapter.setPresenter(p);
        assertEquals(p, adapter.getPresenter());

        Decorator d = Mockito.mock(Decorator.class);
        adapter.setDecorator(d);
        assertNotNull(adapter.mDecorator);
    }
}