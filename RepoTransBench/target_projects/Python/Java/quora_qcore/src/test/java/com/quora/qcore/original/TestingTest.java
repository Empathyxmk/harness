package com.quora.qcore.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestingTest {
    @Test
    public void testAnything() {
        Object anything = null;
        assertEquals(null, anything);
        assertEquals(anything, null);
        assertTrue(anything == null);
    }
    @Test
    public void testGreaterEq() {
        int val = 3;
        assertTrue(val >= 2);
        assertThrows(AssertionError.class, () -> assertTrue(2 > 3));
    }
    @Test
    public void testDisabled() {
        // Disabled tests in Java: Use @Disabled or skip via assumption if needed
    }
}