package com.birin.gridlistviewadapters.utils;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PositionCalculatorPublicTest {

    @Test
    void testCalculateRowIndexPublic() {
        assertEquals(2, PositionCalculator.calculateRowIndex(10, 4)); // 10/4 = 2
    }

    @Test
    void testCalculateColumnIndexPublic() {
        assertEquals(3, PositionCalculator.calculateColumnIndex(7, 4)); // 7%4=3
    }
}