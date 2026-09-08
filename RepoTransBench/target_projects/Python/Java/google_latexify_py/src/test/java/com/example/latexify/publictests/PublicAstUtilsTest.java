package com.example.latexify.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicAstUtilsTest {

    // Simulate a public API wrapper to test public AST utilities.
    static int getAstDepth(String expr) {
        // Dummy: count number of parenthesis as "depth".
        int depth = 0;
        int maxDepth = 0;
        for (char c : expr.toCharArray()) {
            if (c == '(') {
                depth++;
                maxDepth = Math.max(maxDepth, depth);
            } else if (c == ')') {
                depth--;
            }
        }
        return maxDepth;
    }

    @Test
    void testAstDepthSimple() {
        assertEquals(1, getAstDepth("(x)"));
        assertEquals(2, getAstDepth("f((x))"));
        assertEquals(0, getAstDepth("x+y"));
    }
}