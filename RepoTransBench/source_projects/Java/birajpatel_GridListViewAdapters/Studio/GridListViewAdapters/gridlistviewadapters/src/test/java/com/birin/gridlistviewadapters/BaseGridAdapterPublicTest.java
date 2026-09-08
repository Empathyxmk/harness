package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Public test for BaseGridAdapter - using different parameters.
 */
public class BaseGridAdapterPublicTest {

    private static class DummyGridAdapter extends BaseGridAdapter {
        public DummyGridAdapter() {
            super(null, 3, 4); // public test: 3 columns, 4 rows
        }
    }

    private DummyGridAdapter adapter;

    @BeforeEach
    public void setUp() {
        adapter = new DummyGridAdapter();
    }

    @Test
    public void testGetCount() {
        adapter.getCount();
    }

    @Test
    public void testGetNumOfColumns() {
        adapter.getNumOfColumns();
    }

    @Test
    public void testGetNumOfRows() {
        adapter.getNumOfRows();
    }
}