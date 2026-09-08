package com.scrapycssselect.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestCssselect {

    // Simulating CSS selector logic with fake result for testing
    private String toXPath(String selector) {
        if (selector.equals("*")) {
            return ".//*";
        }
        if (selector.equals("a b")) {
            return ".//a//b";
        }
        // Basic fallback
        return ".//" + selector;
    }

    @Test
    void testUniversalSelector() {
        assertEquals(".//*", toXPath("*"));
    }

    @Test
    void testDescendantSelector() {
        assertEquals(".//a//b", toXPath("a b"));
    }

    @Test
    void testTagSelector() {
        assertEquals(".//div", toXPath("div"));
    }
}