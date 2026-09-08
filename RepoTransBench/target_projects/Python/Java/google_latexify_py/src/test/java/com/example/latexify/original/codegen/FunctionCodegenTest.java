package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FunctionCodegenTest {

    static String codegenFunction(String name, String body) {
        return name + "() = " + body;
    }

    @Test
    void testCodegenFunction() {
        assertEquals("f() = x+1", codegenFunction("f", "x+1"));
    }
}