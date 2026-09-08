package com.example.public_tests.handlers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicAwsHandler {
    @Test
    void testAwsEventHandles() {
        assertEquals("AWS:foo", awsHandle("foo"));
    }

    // Simulated AWS handler
    private String awsHandle(String event) { return "AWS:" + event; }
}