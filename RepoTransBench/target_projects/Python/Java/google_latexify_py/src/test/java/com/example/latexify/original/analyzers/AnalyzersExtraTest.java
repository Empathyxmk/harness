package com.example.latexify.original.analyzers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AnalyzersExtraTest {
    static boolean isSubtraction(String expr) {
        return expr.matches("\\d+\\s*-\\s*\\d+");
    }

    @Test
    void testIsSubtraction() {
        assertTrue(isSubtraction("3-2"));
        assertTrue(isSubtraction("10 - 8"));
        assertFalse(isSubtraction("5+3"));
    }
}