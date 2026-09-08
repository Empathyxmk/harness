package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExpressionCodegenTest {

    static String wrapParens(String expr) {
        return "(" + expr + ")";
    }

    @Test
    void testWrapParens() {
        assertEquals("(a+b)", wrapParens("a+b"));
        assertEquals("(x)", wrapParens("x"));
    }
}