package com.tiddl.public_tests;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsTest {

    static class PubUtils {
        static String safeFilename(String s) {
            if (s == null) return "";
            return s.replaceAll("[/:*?\"<>|]", "");
        }
    }

    @Test
    void test_safe_filename_public() {
        String a = "foo/bar:baz?*<>|";
        String res = PubUtils.safeFilename(a);
        assertFalse(res.contains("/"));
        assertFalse(res.contains(":"));
        assertFalse(res.contains("?"));
        assertFalse(res.contains("<"));
        assertFalse(res.contains(">"));
        assertFalse(res.contains("|"));
    }
}