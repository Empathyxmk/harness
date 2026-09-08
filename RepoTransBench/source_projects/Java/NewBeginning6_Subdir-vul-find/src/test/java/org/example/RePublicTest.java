package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class RePublicTest {

    @Test
    void testEscapeAndPattern() {
        String input = "x.y$^";
        String escaped = Re.escape(input);
        assertNotNull(escaped);

        String pattern = "\\d+";
        assertTrue(Re.pattern(pattern, "2024"));
        assertFalse(Re.pattern(pattern, "test"));
        assertFalse(Re.pattern("abc.*", "xyz"));
    }

    @Test
    void testContains() {
        assertTrue(Re.contains("Goodbye moon", "moon"));
        assertFalse(Re.contains("Goodbye", "sun"));
        assertFalse(Re.contains(null, "def"));
        assertFalse(Re.contains("def", null));
        assertFalse(Re.contains(null, null));
    }
}