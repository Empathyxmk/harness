package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicDocumentMatchersModuleTest {
    @Test
    void testPublicMatcher() {
        Matcher matcher = new Matcher("Normal");
        assertTrue(matcher.matches("Normal"));
        assertFalse(matcher.matches("Other"));
    }

    static class Matcher {
        private final String style;
        Matcher(String style) { this.style = style; }
        boolean matches(String input) {
            if (input == null) return false;
            return style.equals(input);
        }
    }
}