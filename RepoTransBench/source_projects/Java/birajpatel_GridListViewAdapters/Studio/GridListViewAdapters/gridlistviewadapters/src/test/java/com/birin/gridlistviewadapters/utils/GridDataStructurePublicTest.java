package com.birin.gridlistviewadapters.utils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GridDataStructurePublicTest {
    @Test
    void testGetSetItemPublic() {
        GridDataStructure<String> grid = new GridDataStructure<>(3, 3);
        grid.setItem(2, 1, "GridTest");
        assertEquals("GridTest", grid.getItem(2, 1));
    }

    @Test
    void testGetNumRowsColsPublic() {
        GridDataStructure<String> grid = new GridDataStructure<>(2, 5);
        assertEquals(2, grid.getNumRows());
        assertEquals(5, grid.getNumColumns());
    }
}