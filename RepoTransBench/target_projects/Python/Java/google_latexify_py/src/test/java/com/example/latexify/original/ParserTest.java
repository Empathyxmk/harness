package com.example.latexify.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ParserTest {
    // Simulate a minimal parser for math expressions
    // The real implementation parses Python AST; here, a dummy parser.

    static class MathParseResult {
        String raw;
        boolean valid;

        MathParseResult(String raw, boolean valid) {
            this.raw = raw;
            this.valid = valid;
        }
    }

    static MathParseResult parse(String expr) {
        // Dummy logic: valid if only contains valid characters.
        if (expr.matches("^[a-zA-Z0-9=+\\-*/^ ().]*$")) {
            return new MathParseResult(expr, true);
        } else {
            return new MathParseResult(expr, false);
        }
    }

    @Test
    void testParseValidExpression() {
        MathParseResult result = parse("f(x)=x^2+1");
        assertTrue(result.valid);
        assertEquals("f(x)=x^2+1", result.raw);
    }

    @Test
    void testParseInvalidExpression() {
        MathParseResult result = parse("f(x)==x^2+1?!");
        assertFalse(result.valid);
        assertEquals("f(x)==x^2+1?!", result.raw);
    }
}