package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {
    int max(int a, int b) {
        return Math.max(a, b);
    }

    int sum(int[] arr) {
        return Arrays.stream(arr).sum();
    }

    @Test
    void testMaxUtil() {
        assertEquals(5, max(2, 5));
        assertEquals(7, max(7, 3));
    }

    @Test
    void testSumUtil() {
        assertEquals(6, sum(new int[]{1, 2, 3}));
        assertEquals(0, sum(new int[]{}));
    }
}