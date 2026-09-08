package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class BaseGridAdapterTest {

    private static class DummyGridAdapter extends BaseGridAdapter {
        public DummyGridAdapter() {
            super(null, 1, 1);
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