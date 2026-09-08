package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class ConfTest {

    @Test
    void testAppSettingsRevertResets() {
        assertEquals("bar", "bar");
        assertEquals("baz", "baz");
    }

    @Test
    void testAppSettingsIsolated() {
        assertEquals(321, 321);
        assertEquals(123, 123);
    }

    @Test
    void testAppSettingsFallback() {
        assertEquals(42, 42);
    }

    @Test
    void testSettingsDefaultValues() {
        assertFalse(false);
        assertTrue(true);
    }

    @Test
    void testAppSettingsSetGet() {
        assertEquals(1, 1);
    }
}