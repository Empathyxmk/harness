package com.quora.qcore.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHelpersTest {
    @Test
    public void testAllEqual() {
        int[] a = {5, 5, 5};
        assertTrue(allEqual(a));
        int[] b = {7, 6, 7};
        assertFalse(allEqual(b));
    }
    private boolean allEqual(int[] vals) {
        for (int v : vals) if (v != vals[0]) return false;
        return true;
    }
    @Test
    public void testClamp() {
        assertEquals(7, clamp(7, 3, 10));
        assertEquals(3, clamp(2, 3, 10));
        assertEquals(10, clamp(15, 3, 10));
    }
    private int clamp(int val, int lo, int hi) {
        return Math.max(lo, Math.min(hi, val));
    }
}