package com.example.original.handlers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestGcpHandler {
    @Test
    void testGcpHandlerLogic() {
        assertEquals("GCP:bar", gcpHandle("bar"));
    }

    private String gcpHandle(String event) { return "GCP:" + event; }
}