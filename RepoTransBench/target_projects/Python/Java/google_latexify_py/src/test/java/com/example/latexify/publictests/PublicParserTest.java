package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicParserTest {
    // Dummy parser for public tests.

    static boolean parseExpression(String s) {
        // Accepts well-formed equations: only letters, digits, +, -, *, /, ^, =.
        return s.matches("^[a-zA-Z0-9=+\\-*/^ ]+$");
    }

    @Test
    void testParserAcceptsValid() {
        assertTrue(parseExpression("f(x)=x^2+1"));
    }

    @Test
    void testParserRejectsInvalid() {
        assertFalse(parseExpression("f(x)=x^2+1$!"));
        assertTrue(parseExpression("a+b=c"));
    }
}