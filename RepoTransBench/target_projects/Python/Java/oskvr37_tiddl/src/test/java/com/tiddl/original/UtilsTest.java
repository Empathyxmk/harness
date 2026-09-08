package com.tiddl.original;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {
    static class Utils {
        static String safeFilename(String s) {
            if (s == null) return "";
            return s.replaceAll("[/:*?\"<>|]", "");
        }
        static int clamp(int val, int min, int max) {
            return Math.max(min, Math.min(max, val));
        }
    }

    @Test
    void test_safe_filename_removes_forbidden_chars() {
        String bad = "a:b*c?d|e<f>g/h\\i\"";
        String result = Utils.safeFilename(bad);
        assertFalse(result.contains(":"));
        assertFalse(result.contains("*"));
        assertFalse(result.contains("?"));
        assertFalse(result.contains("|"));
        assertFalse(result.contains("<"));
        assertFalse(result.contains(">"));
        assertFalse(result.contains("/"));
        assertFalse(result.contains("\\"));
        assertFalse(result.contains("\""));
    }

    @Test
    void test_safe_filename_null_empty() {
        assertEquals("", Utils.safeFilename(null));
        assertEquals("", Utils.safeFilename(""));
    }

    @Test
    void test_clamp_in_range() {
        assertEquals(5, Utils.clamp(5, 0, 10));
    }

    @Test
    void test_clamp_below() {
        assertEquals(0, Utils.clamp(-20, 0, 10));
    }

    @Test
    void test_clamp_above() {
        assertEquals(10, Utils.clamp(20, 0, 10));
    }
}