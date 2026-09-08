package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicLogicTest {
    boolean isEven(int n) { return n % 2 == 0; }
    boolean isPositive(int n) { return n > 0; }
    boolean logicalAnd(boolean a, boolean b) { return a && b; }
    boolean logicalOr(boolean a, boolean b) { return a || b; }

    @Test
    void testLogicAnd() {
        assertTrue(logicalAnd(isEven(4), isPositive(4)));
        assertFalse(logicalAnd(isEven(5), isPositive(5)));
    }

    @Test
    void testLogicOr() {
        assertTrue(logicalOr(isEven(4), isPositive(-4)));
        assertFalse(logicalOr(isEven(5), isPositive(-5)));
    }
}