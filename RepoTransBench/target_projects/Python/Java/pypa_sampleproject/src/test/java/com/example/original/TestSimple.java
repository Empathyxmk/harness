package com.example.original;

import static org.junit.jupiter.api.Assertions.*;

import com.example.sample.Simple;
import org.junit.jupiter.api.Test;

class TestSimple {

    @Test
    void testAddOnePositive() {
        assertEquals(3, Simple.addOne(2));
    }

    @Test
    void testAddOneZero() {
        assertEquals(1, Simple.addOne(0));
    }

    @Test
    void testAddOneNegative() {
        assertEquals(-4, Simple.addOne(-5));
    }

    @Test
    void testAddOneFloat() {
        assertEquals(3.5, Simple.addOne(2.5), 1e-8);
    }

    @Test
    void testAddOneStrRaises() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            Simple.addOne("hi");
        });
        assertTrue(exception.getMessage().contains("int or double"));
    }
}