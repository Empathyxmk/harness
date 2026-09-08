package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SetupPyTest {
    @Test
    void testPackageName() {
        Setup setup = new Setup("mammoth", "1.0.0");
        assertEquals("mammoth", setup.getName());
        assertEquals("1.0.0", setup.getVersion());
    }

    static class Setup {
        private final String name;
        private final String version;
        Setup(String name, String version) { this.name = name; this.version = version; }
        String getName() { return name; }
        String getVersion() { return version; }
    }
}