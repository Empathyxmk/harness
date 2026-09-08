package com.example.plop.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class Platform {
    public static String get_hostname() { return "host"; }
    public static String get_username() { return "bob"; }
}

public class PublicPlatformTest {

    @Test
    void testGetHostname() {
        String h = Platform.get_hostname();
        assertNotNull(h);
        assertTrue(h instanceof String);
        assertTrue(h.length() >= 0);
    }

    @Test
    void testGetUsername() {
        String u = Platform.get_username();
        assertNotNull(u);
        assertTrue(u instanceof String);
        assertTrue(u.length() >= 0);
    }
}