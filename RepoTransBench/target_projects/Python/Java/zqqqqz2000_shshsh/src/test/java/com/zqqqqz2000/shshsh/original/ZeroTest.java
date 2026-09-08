package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ZeroTest {
    int countZeros(int[] arr) {
        int count = 0;
        for (int a : arr) if (a == 0) count++;
        return count;
    }

    @Test
    void testCountZerosInArray() {
        assertEquals(1, countZeros(new int[]{5, 0, 7}));
        assertEquals(0, countZeros(new int[]{1, 2, 3}));
        assertEquals(3, countZeros(new int[]{0, 0, 0}));
    }
}