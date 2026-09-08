package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class LogicTest {
    private boolean isEven(int n) {
        return n % 2 == 0;
    }

    private boolean isOdd(int n) {
        return n % 2 != 0;
    }

    @Test
    void testIsEven() {
        assertTrue(isEven(2));
        assertFalse(isEven(3));
        assertTrue(isEven(100));
        assertFalse(isEven(101));
    }

    @Test
    void testIsOdd() {
        assertFalse(isOdd(2));
        assertTrue(isOdd(3));
        assertFalse(isOdd(100));
        assertTrue(isOdd(101));
    }
}