package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicMiddlewareCore {
    @Test
    void testCall() {
        Middleware mw = new Middleware();
        assertEquals("called", mw.handle());
    }

    // Minimal "middleware" for demonstration
    private static class Middleware {
        String handle() { return "called"; }
    }
}