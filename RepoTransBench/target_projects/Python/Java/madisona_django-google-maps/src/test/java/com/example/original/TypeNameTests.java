package com.example.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class TypeNameTests {

    // Simulate the typename() functionality as described in the Python test
    public static String typename(Object obj) {
        if (obj instanceof String) return "str";
        if (obj instanceof Class<?>) return "type";
        return obj.getClass().getSimpleName();
    }

    @Test
    void testSimpleTypeReturnsTypeNameAsString() {
        assertEquals("str", typename("x"));
    }

    @Test
    void testClassObject() {
        class X {}
        assertEquals("type", typename(X.class));
    }
}