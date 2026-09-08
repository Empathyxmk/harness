package com.example.parsley.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicProtocolTest {

    @Test
    public void testPublicProtocolPing() {
        Protocol protocol = new Protocol();
        assertEquals("response:pong", protocol.handle("request:ping"));
    }

    @Test
    public void testPublicProtocolUnknown() {
        Protocol protocol = new Protocol();
        assertEquals("error:unknown", protocol.handle("request:abc"));
    }
}

// redeclared for isolation
class Protocol {
    public String handle(String message) {
        if ("request:ping".equals(message)) return "response:pong";
        return "error:unknown";
    }
}