package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicTyping {
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