package com.example.original.handlers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestLocalHandler {
    @Test
    void testLocalHandlerLogic() {
        assertEquals("LOCAL:baz", localHandle("baz"));
    }

    private String localHandle(String event) { return "LOCAL:" + event; }
}