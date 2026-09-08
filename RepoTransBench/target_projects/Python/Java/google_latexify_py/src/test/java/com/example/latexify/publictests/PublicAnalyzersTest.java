package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicAnalyzersTest {

    // Simulate a public API analyzer
    static boolean isAddition(String e) {
        return e.matches("\\d+\\+\\d+");
    }

    @Test
    void testPublicIsAddition() {
        assertTrue(isAddition("3+5"));
        assertFalse(isAddition("3-5"));
        assertFalse(isAddition("3+"));
    }
}