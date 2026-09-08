package com.vijos.jd4.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicCompareTest {

    static String stripTrailingSpacesNewlines(String s) {
        return s.stripTrailing();
    }

    static boolean compare(String a, String b, boolean ignoreTrailingSpaces) {
        if (ignoreTrailingSpaces)
            return a.strip().equals(b.strip());
        return a.equals(b);
    }

    @Test
    void testStripTrailingSpacesNewlinesPublic() {
        String s = "hello world    \n  \n\t";
        assertEquals("hello world", stripTrailingSpacesNewlines(s));
    }

    @Test
    void testComparePublicEqualNorm() {
        String a = "foo bar   \n";
        String b = "foo bar";
        assertTrue(compare(a, b, true));
    }

    @Test
    void testComparePublicNotEqual() {
        String a = "value1";
        String b = "value2";
        assertFalse(compare(a, b, false));
    }
}