package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DocumentMatchersModuleTest {
    @Test
    void testMatcherMatchesHeading() {
        Matcher matcher = new Matcher("Heading1");
        assertTrue(matcher.matches("Heading1"));
        assertFalse(matcher.matches("Heading2"));
    }

    @Test
    void testMatcherNullReturnsFalse() {
        Matcher matcher = new Matcher("Heading1");
        assertFalse(matcher.matches(null));
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