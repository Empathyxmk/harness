package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExpressionRulesTest {

    static boolean hasAddition(String expr) {
        return expr.contains("+");
    }

    @Test
    void testHasAddition() {
        assertTrue(hasAddition("x+y"));
        assertFalse(hasAddition("xy"));
    }
}