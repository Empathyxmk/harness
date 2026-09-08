package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSetupPyTest {
    @Test
    void testPublicSetup() {
        Setup setup = new Setup("publicLib", "2.3.4");
        assertEquals("publicLib", setup.getName());
        assertEquals("2.3.4", setup.getVersion());
    }

    static class Setup {
        private final String name;
        private final String version;
        Setup(String name, String version) { this.name = name; this.version = version; }
        String getName() { return name; }
        String getVersion() { return version; }
    }
}