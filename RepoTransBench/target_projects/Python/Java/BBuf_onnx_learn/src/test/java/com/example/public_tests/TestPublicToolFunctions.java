package com.example.public_tests;

import com.example.tools.tool.Functions;
import com.example.tools.tool.Tool;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicToolFunctions {

    @Test
    void testAdd() {
        assertEquals(12, Functions.add(5, 7));
        assertEquals(0, Functions.add(-3, 3));
        assertEquals(0, Functions.add(10, -10));
    }

    @Test
    void testSub() {
        assertEquals(8, Functions.sub(10, 2));
        assertEquals(-15, Functions.sub(-10, 5));
    }

    @Test
    void testMul() {
        assertEquals(21, Functions.mul(7, 3));
        assertEquals(-8, Functions.mul(-4, 2));
    }

    @Test
    void testDiv() {
        assertEquals(4, Functions.div(8, 2));
        Exception exception = assertThrows(ArithmeticException.class, () -> Functions.div(-4, 0));
        assertEquals("division by zero", exception.getMessage());
    }

    @Test
    void testToolClass() {
        Tool t = new Tool();
        assertEquals(-8, t.multiply(4, -2));
        assertEquals(0, t.identity(0));
        assertTrue(t.identity(123) instanceof Integer);
    }
}