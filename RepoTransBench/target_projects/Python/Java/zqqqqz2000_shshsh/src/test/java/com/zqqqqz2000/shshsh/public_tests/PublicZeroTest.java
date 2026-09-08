package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicZeroTest {
    @Test
    void testZeroAddition() {
        assertEquals(0, 0+0);
        assertEquals(3, 3+0);
        assertEquals(-9, -9+0);
    }

    @Test
    void testZeroMultiplication() {
        assertEquals(0, 3*0);
        assertEquals(0, 0*12345);
        assertEquals(0, -8*0);
    }
}