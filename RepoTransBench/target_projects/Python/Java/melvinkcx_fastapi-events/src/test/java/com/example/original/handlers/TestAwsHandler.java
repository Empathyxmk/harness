package com.example.original.handlers;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestAwsHandler {
    @Test
    void testAwsEventHandles() {
        assertEquals("AWS:foo", awsHandle("foo"));
    }

    private String awsHandle(String event) { return "AWS:" + event; }
}