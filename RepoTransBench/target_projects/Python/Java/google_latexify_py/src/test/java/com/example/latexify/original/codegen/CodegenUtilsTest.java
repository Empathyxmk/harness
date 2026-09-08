package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CodegenUtilsTest {

    static boolean endsWithSemicolon(String code) {
        return code.trim().endsWith(";");
    }

    @Test
    void testEndsWithSemicolon() {
        assertTrue(endsWithSemicolon("x = 1;"));
        assertFalse(endsWithSemicolon("x = 1"));
    }
}