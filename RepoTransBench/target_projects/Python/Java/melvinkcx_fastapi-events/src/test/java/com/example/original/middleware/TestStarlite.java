package com.example.original.middleware;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestStarlite {
    @Test
    void testStarliteHandlesEvent() {
        assertEquals("STARLITE:eventX", starliteHandle("eventX"));
    }

    private String starliteHandle(String event) { return "STARLITE:" + event; }
}