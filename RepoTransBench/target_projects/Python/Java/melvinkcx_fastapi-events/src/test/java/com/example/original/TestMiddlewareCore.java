package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestMiddlewareCore {
    @Test
    void testCall() {
        Middleware mw = new Middleware();
        assertEquals("called", mw.handle());
    }

    private static class Middleware {
        String handle() { return "called"; }
    }
}