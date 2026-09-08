package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestTyping {
    enum SomeType { X, Y }
    @Test
    void testEnumValue() {
        assertEquals("X", SomeType.X.name());
    }

    @Test
    void testEnumSize() {
        assertEquals(2, SomeType.values().length);
    }
}