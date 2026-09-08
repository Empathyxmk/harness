package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PrefixTrimmerTest {
    static String trimPrefix(String code, String prefix) {
        if (code.startsWith(prefix)) {
            return code.substring(prefix.length());
        }
        return code;
    }

    @Test
    void testTrimPrefix() {
        assertEquals("bar", trimPrefix("foobar", "foo"));
        assertEquals("foobar", trimPrefix("foobar", "baz")); // unchanged
    }
}