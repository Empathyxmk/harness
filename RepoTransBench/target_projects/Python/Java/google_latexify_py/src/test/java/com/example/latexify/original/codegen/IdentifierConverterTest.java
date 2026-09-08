package com.example.latexify.original.codegen;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IdentifierConverterTest {

    static String toSnakeCase(String camel) {
        return camel.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase();
    }

    @Test
    void testToSnakeCase() {
        assertEquals("foo_bar", toSnakeCase("FooBar"));
        assertEquals("x", toSnakeCase("x"));
    }
}