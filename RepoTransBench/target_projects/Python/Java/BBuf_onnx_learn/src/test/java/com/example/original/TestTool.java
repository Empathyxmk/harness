package com.example.original;

import com.example.tools.tool.Functions;
import com.example.tools.tool.Tool;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestTool {

    @Test
    void testAdd() {
        assertEquals(3, Functions.add(1, 2));
        assertEquals(0, Functions.add(-2, 2));
        assertEquals(0, Functions.add(0, 0));
    }

    @Test
    void testSub() {
        assertEquals(1, Functions.sub(3, 2));
        assertEquals(-2, Functions.sub(-1, 1));
    }

    @Test
    void testMul() {
        assertEquals(6, Functions.mul(3, 2));
        assertEquals(0, Functions.mul(0, 8));
    }

    @Test
    void testDiv() {
        assertEquals(2, Functions.div(6, 3));
        Exception exception = assertThrows(ArithmeticException.class, () -> Functions.div(3, 0));
        assertEquals("division by zero", exception.getMessage());
    }

    @Test
    void testToolClass() {
        Tool t = new Tool();
        assertEquals(6, t.multiply(2, 3));
        assertEquals(10, t.identity(10));
        assertTrue(t.identity(5) instanceof Integer);
    }
}