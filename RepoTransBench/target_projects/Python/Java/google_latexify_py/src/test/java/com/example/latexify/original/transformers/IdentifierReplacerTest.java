package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IdentifierReplacerTest {
    static String replaceID(String code, String oldName, String newName) {
        return code.replace(oldName, newName);
    }

    @Test
    void testReplaceID() {
        assertEquals("foo = bar + 1", replaceID("x = bar + 1", "x", "foo"));
        assertEquals("a = x + 1", replaceID("a = x + 1", "z", "b")); // nothing replaced
    }
}