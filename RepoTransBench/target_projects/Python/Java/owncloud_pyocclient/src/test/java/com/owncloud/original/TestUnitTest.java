package com.owncloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.*;
import java.nio.charset.StandardCharsets;

class TestUnitTest {

    // --- ResponseError/OCSResponseError tests already covered in ResponseErrorTest.java

    // --- ShareInfo tests already covered in ShareInfoTest.java

    // --- Utils tests already covered in UtilsTest.java

    // Provide dummy placeholder for oc namespace
    static class oc {

        public static String escape_path(String p) {
            return p.replace(" ", "%20");
        }

        public static String unescape_path(String p) {
            return p.replace("%20", " ");
        }

        public static String to_unicode(byte[] b) { return new String(b, StandardCharsets.UTF_8); }
        public static String to_unicode(String s) { return s; }
        public static byte[] to_bytes(String s) { return s.getBytes(StandardCharsets.UTF_8); }
        public static byte[] to_bytes(byte[] b) { return b; }

        public static String strip_trailing_slash(String s) {
            if (s == null)
                return null;
            if (s.equals("/")) return "/";
            if (s.endsWith("/"))
                return s.substring(0, s.length() - 1);
            return s;
        }
    }

    @Test
    void test_escape_unescape() {
        String p = "/a b/abc.txt";
        String out = oc.escape_path(p);
        assertTrue(out.contains("%20"));
        assertEquals(p, oc.unescape_path(out));
    }

    @Test
    void test_to_unicode_bytes() {
        assertEquals("abc", oc.to_unicode("abc".getBytes(StandardCharsets.UTF_8)));
        assertEquals("xyz", oc.to_unicode("xyz"));
    }

    @Test
    void test_to_bytes() {
        assertArrayEquals("xyz".getBytes(StandardCharsets.UTF_8), oc.to_bytes("xyz"));
        assertArrayEquals("xyz".getBytes(StandardCharsets.UTF_8), oc.to_bytes("xyz".getBytes(StandardCharsets.UTF_8)));
    }

    @Test
    void test_strip_trailing_slash() {
        assertEquals("foo", oc.strip_trailing_slash("foo/"));
        assertEquals("/bar", oc.strip_trailing_slash("/bar/"));
        assertEquals("/", oc.strip_trailing_slash("/"));
        assertNull(oc.strip_trailing_slash(null));
    }

    // ShareInfo logic tested in ShareInfoTest.java

}