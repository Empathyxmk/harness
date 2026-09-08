package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.Test;

// Public test for ListGridAdapter - testing with different constructor values.
public class ListGridAdapterPublicTest {

    private static class DummyListGridAdapter extends ListGridAdapter {
        public DummyListGridAdapter() {
            super(null, 2, 3); // public test uses different # cols/rows
        }
    }

    @Test
    public void testInstantiation() {
        DummyListGridAdapter adapter = new DummyListGridAdapter();
        adapter.getCount();
        adapter.getNumOfRows();
        adapter.getNumOfColumns();
    }
}