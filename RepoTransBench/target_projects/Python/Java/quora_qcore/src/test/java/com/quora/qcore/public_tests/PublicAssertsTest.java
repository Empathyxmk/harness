package com.quora.qcore.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicAssertsTest {
    @Test
    public void testAssertEq() {
        assertEquals(2, 2);
        assertEquals("xyz", "xyz");
        assertEquals(3.149, 3.15, 0.01);
    }
    @Test
    public void testAssertFails() {
        assertThrows(AssertionError.class, () -> assertEquals(1, 3));
    }
    @Test
    public void testOrdering() {
        assertTrue(5 > 3);
        assertThrows(AssertionError.class, () -> assertTrue(3 > 3));
    }
    @Test
    public void testContains() {
        assertTrue("foobar".contains("bar"));
        assertFalse("foobar".contains("baz"));
    }
}