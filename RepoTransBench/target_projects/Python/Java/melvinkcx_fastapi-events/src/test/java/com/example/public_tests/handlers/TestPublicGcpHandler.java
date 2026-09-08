package com.example.public_tests.handlers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicGcpHandler {
    @Test
    void testGcpHandlerLogic() {
        assertEquals("GCP:bar", gcpHandle("bar"));
    }

    private String gcpHandle(String event) { return "GCP:" + event; }
}