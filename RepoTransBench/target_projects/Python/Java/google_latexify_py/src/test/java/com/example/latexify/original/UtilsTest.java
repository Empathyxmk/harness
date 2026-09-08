package com.example.latexify.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    static String removeWhitespace(String s) {
        return s.replaceAll("\\s+", "");
    }

    @Test
    void testRemoveWhitespace() {
        assertEquals("abc", removeWhitespace("a b     c  "));
        assertEquals("", removeWhitespace("    "));
        assertEquals("foo", removeWhitespace("foo"));
    }

    @Test
    void testRemoveWhitespaceWithTabsAndNewlines() {
        assertEquals("a", removeWhitespace("\t\n  a \n\t"));
    }
}