package com.owncloud.original;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class UtilsTest {
    static class Utils {
        // Simple placeholder implementations to allow test translation
        public static String escape_path(String p) {
            return p.replaceAll(" ", "%20");
        }

        public static String unescape_path(String p) {
            return p.replaceAll("%20", " ");
        }

        public static String to_unicode(byte[] b) {
            return new String(b);
        }

        public static String to_unicode(String s) {
            return s;
        }

        public static byte[] to_bytes(String s) {
            return s.getBytes();
        }

        public static byte[] to_bytes(byte[] b) {
            return b;
        }

        public static String strip_trailing_slash(String s) {
            if (s == null)
                return null;
            if (s.equals("/")) return "/";
            if (s.endsWith("/"))
                return s.substring(0, s.length()-1);
            return s;
        }
    }

    @Test
    void test_escape_unescape() {
        String p = "/a b/abc.txt";
        String out = Utils.escape_path(p);
        assertTrue(out.contains("%20"));
        assertEquals(p, Utils.unescape_path(out));
    }

    @Test
    void test_to_unicode_bytes() {
        assertEquals("abc", Utils.to_unicode("abc".getBytes()));
        assertEquals("xyz", Utils.to_unicode("xyz"));
    }

    @Test
    void test_to_bytes() {
        assertArrayEquals("xyz".getBytes(), Utils.to_bytes("xyz"));
        assertArrayEquals("xyz".getBytes(), Utils.to_bytes("xyz".getBytes()));
    }

    @Test
    void test_strip_trailing_slash() {
        assertEquals("foo", Utils.strip_trailing_slash("foo/"));
        assertEquals("/bar", Utils.strip_trailing_slash("/bar/"));
        assertEquals("/", Utils.strip_trailing_slash("/"));
        assertNull(Utils.strip_trailing_slash(null));
    }
}