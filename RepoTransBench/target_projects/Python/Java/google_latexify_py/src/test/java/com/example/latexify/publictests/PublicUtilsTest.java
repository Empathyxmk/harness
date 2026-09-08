package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsTest {

    static String stripWhitespace(String s) {
        return s.replaceAll("\\s+", "");
    }

    @Test
    void testStripWhitespace() {
        assertEquals("abc", stripWhitespace("a b  c"));
        assertEquals("", stripWhitespace("     "));
    }
}