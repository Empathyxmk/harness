package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsTest {
    int factorial(int n) {
        if (n < 2) return 1;
        return n * factorial(n - 1);
    }

    String pad(String s, int width) {
        return String.format("%" + width + "s", s);
    }

    @Test
    void testFactorial() {
        assertEquals(1, factorial(0));
        assertEquals(1, factorial(1));
        assertEquals(2, factorial(2));
        assertEquals(6, factorial(3));
        assertEquals(24, factorial(4));
        assertEquals(120, factorial(5));
    }

    @Test
    void testPad() {
        assertEquals("   hi", pad("hi", 5));
        assertEquals("test", pad("test", 4));
        assertEquals("test", pad("test", 2));
    }
}