package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicQuickManualTest {
    int inc(int n) { return n + 1; }
    int dec(int n) { return n - 1; }

    @Test
    void testQuickManualInc() {
        assertEquals(6, inc(5));
        assertEquals(-1, inc(-2));
    }

    @Test
    void testQuickManualDec() {
        assertEquals(4, dec(5));
        assertEquals(-3, dec(-2));
    }
}