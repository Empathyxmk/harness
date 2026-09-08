package com.github.markzhai.recyclerview;

import android.content.Context;
import android.databinding.ViewDataBinding;
import android.view.LayoutInflater;
import android.view.ViewGroup;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Public test with different data for BaseViewAdapter.
 */
public class BaseViewAdapterPublicTest {

    private Context context;
    private LayoutInflater inflater;

    private static class TestAdapter extends BaseViewAdapter<String> {
        public TestAdapter(Context context) { super(context); }

        @Override
        public BindingViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            return null;
        }
    }

    @Before
    public void setUp() {
        context = Mockito.mock(Context.class);
        inflater = Mockito.mock(LayoutInflater.class);
        Mockito.when(context.getSystemService(Context.LAYOUT_INFLATER_SERVICE)).thenReturn(inflater);
    }

    @Test
    public void testAddSetClearPublic() {
        TestAdapter adapter = new TestAdapter(context);

        // Using different data set
        adapter.add("red");
        assertEquals(1, adapter.getItemCount());
        adapter.set(Arrays.asList("yellow", "green", "blue"));
        assertEquals(3, adapter.getItemCount());
        adapter.clear();
        assertEquals(0, adapter.getItemCount());
    }

    @Test
    public void testRemoveGetPublic() {
        TestAdapter adapter = new TestAdapter(context);

        adapter.set(Arrays.asList("x", "y", "z"));
        assertEquals("y", adapter.get(1));
        adapter.remove(0);
        assertEquals("y", adapter.get(0));
        assertEquals(2, adapter.getItemCount());
    }
}