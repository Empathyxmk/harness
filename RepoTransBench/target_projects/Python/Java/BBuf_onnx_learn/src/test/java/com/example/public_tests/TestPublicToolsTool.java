package com.example.public_tests;

import com.example.tools.tool.Functions;
import com.example.tools.tool.Tool;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicToolsTool {

    @Test
    void testBasicOps() {
        assertEquals(35, Functions.add(20, 15));
        assertEquals(5, Functions.sub(30, 25));
        assertEquals(6, Functions.mul(6, 1));
        assertEquals(9, Functions.div(81, 9));
    }

    @Test
    void testNegativeValues() {
        assertEquals(-15, Functions.sub(-10, 5));
        assertEquals(-25, Functions.mul(5, -5));
    }

    @Test
    void testDivZero() {
        assertThrows(ArithmeticException.class, () -> Functions.div(-10, 0));
    }

    @Test
    void testToolMultiply() {
        Tool t = new Tool();
        assertEquals(0, t.multiply(9, 0));
    }

    @Test
    void testToolIdentity() {
        Tool t = new Tool();
        // Using Arrays.asList for Java equivalent to Python list
        assertEquals(Arrays.asList(1, "x", 3), t.identity(Arrays.asList(1, "x", 3)));
    }
}