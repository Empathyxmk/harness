package com.example.public_tests.middleware;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicStarlette {
    @Test
    void testStarletteHandlesEvent() {
        assertEquals("STARLETTE:test123", starletteHandle("test123"));
    }

    private String starletteHandle(String event) { return "STARLETTE:" + event; }
}