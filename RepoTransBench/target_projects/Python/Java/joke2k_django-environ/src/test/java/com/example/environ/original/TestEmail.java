package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestEmail {

    @Test
    void testDefaultEmailConfig() {
        EmailConfig email = EmailConfig.defaultEmail();
        assertEquals("smtp", email.getBackend());
    }

    @Test
    void testParseEmailUrl() {
        EmailConfig email = EmailConfig.fromUrl("smtp://user:pass@smtp.server.com:587");
        assertEquals("smtp", email.getBackend());
        assertEquals("user", email.getUser());
        assertEquals("pass", email.getPassword());
        assertEquals("smtp.server.com", email.getHost());
        assertEquals(587, email.getPort());
    }
}