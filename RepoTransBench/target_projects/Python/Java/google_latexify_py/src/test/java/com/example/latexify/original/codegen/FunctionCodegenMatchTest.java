package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FunctionCodegenMatchTest {

    static boolean matchFunctionDef(String code) {
        // checks for "def fname(...)"
        return code.trim().startsWith("def ");
    }

    @Test
    void testMatchFunctionDef() {
        assertTrue(matchFunctionDef("def foo(): pass"));
        assertFalse(matchFunctionDef("foo(): pass"));
    }
}