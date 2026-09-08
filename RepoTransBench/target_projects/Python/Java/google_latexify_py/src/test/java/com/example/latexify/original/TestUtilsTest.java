package com.example.latexify.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestUtilsTest {

    static boolean floatsClose(double a, double b) {
        return Math.abs(a - b) < 1e-7;
    }

    @Test
    void testFloatsCloseSame() {
        assertTrue(floatsClose(1.00000001, 1.00000002));
        assertTrue(floatsClose(0.0, 0.0));
    }

    @Test
    void testFloatsCloseDifferent() {
        assertFalse(floatsClose(0.0, 1.0));
        assertFalse(floatsClose(1.0, 2.0));
    }
}