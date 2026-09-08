package com.quora.qcore.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AssertsTest {
    @Test
    public void testAssertEq() {
        assertEquals(1, 1);
        assertEquals("abc", "abc");
        assertNull(null);
        assertEquals(1.0004, 1.0005, 0.001);
    }

    @Test
    public void testAssertOrdering() {
        assertTrue(2 > 1);
        assertThrows(AssertionError.class, () -> assertTrue(1 > 1));
        assertThrows(AssertionError.class, () -> assertTrue(0 > 1));
        assertTrue(2 >= 1);
        assertTrue(1 >= 1);
        assertThrows(AssertionError.class, () -> assertTrue(0 >= 1));
    }

    @Test
    public void testAssertIn() {
        assertTrue("a".contains("a"));
        assertThrows(AssertionError.class, () -> assertTrue("b".contains("a")));
    }
}