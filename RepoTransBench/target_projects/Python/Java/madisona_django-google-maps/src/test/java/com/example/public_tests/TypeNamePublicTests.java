package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TypeNamePublicTests {
    static String typename(Object obj) {
        if (obj instanceof String) return "str";
        if (obj instanceof Class<?>) return "type";
        return obj.getClass().getSimpleName();
    }

    @Test
    void testSimpleTypeReturnsTypeNameAsStringPublic() {
        assertEquals("str", typename("abc"));
    }

    @Test
    void testClassObjectPublic() {
        class Y {}
        assertEquals("type", typename(Y.class));
    }
}