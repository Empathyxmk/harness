package com.example.original.middleware;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestStarlette {
    @Test
    void testStarletteHandlesEvent() {
        assertEquals("STARLETTE:test123", starletteHandle("test123"));
    }

    private String starletteHandle(String event) { return "STARLETTE:" + event; }
}