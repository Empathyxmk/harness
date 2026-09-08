package com.example.public_tests;

import static org.junit.jupiter.api.Assertions.*;

import com.example.sample.Simple;
import org.junit.jupiter.api.Test;

class PublicSimpleTest {

    @Test
    void testAddOneLargePositive() {
        assertEquals(101, Simple.addOne(100));
    }

    @Test
    void testAddOneNegativeOne() {
        assertEquals(0, Simple.addOne(-1));
    }

    @Test
    void testAddOneLargeNegative() {
        assertEquals(-98, Simple.addOne(-99));
    }

    @Test
    void testAddOneFloatNegative() {
        assertEquals(-1.25, Simple.addOne(-2.25), 1e-8);
    }

    @Test
    void testAddOneNoneRaises() {
        Exception ex = assertThrows(NullPointerException.class, () -> {
            Simple.addOne((Object) null);
        });
        assertTrue(ex.getMessage().contains("Argument cannot be null"));
    }
}