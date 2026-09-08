package com.pyPattyrn.behavioral.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.behavioral.nullpattern.Null;

class NullTest {
    private Null nullObj;

    @BeforeEach
    void setUp() {
        nullObj = new Null();
    }

    @Test
    void testInit() {
        assertNotNull(nullObj);
    }

    @Test
    void testToStringIsBlank() {
        assertEquals("", nullObj.toString());
    }

    @Test
    void testEquality() {
        Null anotherNull = new Null();
        assertEquals(nullObj, anotherNull);
    }

    @Test
    void testIsNullObject() {
        assertTrue(nullObj.isNull());
    }

    @Test
    void testAnyMethodReturnsNull() {
        assertNull(nullObj.someMethod());
    }
}