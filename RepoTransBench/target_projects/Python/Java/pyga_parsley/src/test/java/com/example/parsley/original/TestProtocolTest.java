package com.example.parsley.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestProtocolTest {

    @Test
    public void testRequestResponseCycle() {
        // Simulate a protocol-handler scenario (round-trip)
        Protocol protocol = new Protocol();
        String input = "request:ping";
        String expected = "response:pong";
        assertEquals(expected, protocol.handle(input));
    }

    @Test
    public void testErrorResponse() {
        Protocol protocol = new Protocol();
        String input = "request:foobar";
        String expected = "error:unknown";
        assertEquals(expected, protocol.handle(input));
    }
}

class Protocol {
    public String handle(String message) {
        if ("request:ping".equals(message)) return "response:pong";
        return "error:unknown";
    }
}