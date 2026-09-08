package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ReTest {

    @Test
    void testEscapeAndPattern() {
        String input = "a+b*c";
        String escaped = Re.escape(input);
        assertNotNull(escaped);

        String pattern = "[a-z]+";
        assertTrue(Re.pattern(pattern, "hello"));
        assertFalse(Re.pattern(pattern, "123"));
        assertFalse(Re.pattern(".*", ""));
    }

    @Test
    void testContains() {
        assertTrue(Re.contains("Hello world", "world"));
        assertFalse(Re.contains("Hello", "bye"));
        assertFalse(Re.contains(null, "abc"));
        assertFalse(Re.contains("abc", null));
        assertFalse(Re.contains(null, null));
    }
}