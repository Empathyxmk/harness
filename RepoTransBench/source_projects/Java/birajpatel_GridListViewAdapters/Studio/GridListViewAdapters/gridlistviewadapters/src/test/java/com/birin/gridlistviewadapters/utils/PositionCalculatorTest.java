package com.birin.gridlistviewadapters.utils;

import org.junit.Test;
import static org.junit.Assert.*;

public class PositionCalculatorTest {

    @Test
    public void testGetRowAndColumnIndex() {
        int position = 7, columns = 3;
        int[] res = PositionCalculator.getRowAndColumnIndex(position, columns);
        assertArrayEquals(new int[]{2, 1}, res);
    }

    @Test
    public void testGetPosition() {
        int row = 2, col = 1, columns = 3;
        int position = PositionCalculator.getPosition(row, col, columns);
        assertEquals(7, position);
    }

    @Test
    public void testGetTotalRows() {
        assertEquals(4, PositionCalculator.getTotalRows(10, 3));
    }
}