package com.birin.gridlistviewadapters;

import org.junit.jupiter.api.Test;

// Minimal constructor invocation with different columns/rows
class CursorGridAdapterPublicTest {

    private static class DummyCursorGridAdapter extends CursorGridAdapter {
        public DummyCursorGridAdapter() {
            super(null, 4, 2); // 4 columns, 2 rows (different from any default)
        }
    }

    @Test
    void testInstantiationPublic() {
        DummyCursorGridAdapter adapter = new DummyCursorGridAdapter();
        adapter.getCount();
        adapter.getNumOfRows();
        adapter.getNumOfColumns();
    }
}