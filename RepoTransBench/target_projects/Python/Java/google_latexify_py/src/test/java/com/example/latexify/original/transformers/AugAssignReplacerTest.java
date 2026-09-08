package com.example.latexify.original.transformers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AugAssignReplacerTest {

    static String replaceAugAssign(String code) {
        // replaces "+=" with "= x +"
        return code.replaceAll("(\\w+) \\+= (\\d+)", "$1 = $1 + $2");
    }

    @Test
    void testReplaceAugAssign() {
        assertEquals("x = x + 1", replaceAugAssign("x += 1"));
        assertEquals("x = x + 2", replaceAugAssign("x += 2"));
        assertEquals("a -= 1", replaceAugAssign("a -= 1")); // unchanged
    }
}