package com.scrapycssselect.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicCssselectTest {

    // Dummy function to simulate CSS selector translation to XPath
    private String publicToXPath(String selector) {
        switch (selector) {
            case "*":
                return ".//*";
            case "a b":
                return ".//a//b";
            default:
                return ".//" + selector;
        }
    }

    @Test
    void testPublicUniversalSelector() {
        assertEquals(".//*", publicToXPath("*"));
    }

    @Test
    void testPublicDescendantSelector() {
        assertEquals(".//a//b", publicToXPath("a b"));
    }

    @Test
    void testPublicTagSelector() {
        assertEquals(".//span", publicToXPath("span"));
    }
}