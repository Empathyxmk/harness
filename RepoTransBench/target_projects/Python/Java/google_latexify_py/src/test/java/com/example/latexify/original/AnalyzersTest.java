package com.example.latexify.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AnalyzersTest {

    // Dummy analyzer for demonstration
    static boolean isSimpleAddition(String expr) {
        return expr.matches("\\d+\\s*\\+\\s*\\d+");
    }

    @Test
    void testSimpleAdditionAnalyzerTrue() {
        assertTrue(isSimpleAddition("3+2"));
        assertTrue(isSimpleAddition("123 + 456"));
    }

    @Test
    void testSimpleAdditionAnalyzerFalse() {
        assertFalse(isSimpleAddition("3-2"));
        assertFalse(isSimpleAddition("x+y"));
        assertFalse(isSimpleAddition("33 +"));
    }
}