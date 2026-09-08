package com.example.original;

import com.example.tools.tool.Functions;
import com.example.tools.tool.Tool;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestToolsTool {
    @Test
    void testBasicOps() {
        assertEquals(15, Functions.add(10, 5));
        assertEquals(5, Functions.sub(10, 5));
        assertEquals(0, Functions.mul(4, 0));
        assertEquals(5, Functions.div(20, 4));
    }

    @Test
    void testNegativeValues() {
        assertEquals(0, Functions.sub(-5, -5));
        assertEquals(-6, Functions.mul(-2, 3));
    }

    @Test
    void testDivZero() {
        assertThrows(ArithmeticException.class, () -> Functions.div(1, 0));
    }

    @Test
    void testToolMultiply() {
        Tool t = new Tool();
        assertEquals(-8, t.multiply(-1, 8));
    }

    @Test
    void testToolIdentity() {
        Tool t = new Tool();
        assertEquals("abc", t.identity("abc"));
    }
}