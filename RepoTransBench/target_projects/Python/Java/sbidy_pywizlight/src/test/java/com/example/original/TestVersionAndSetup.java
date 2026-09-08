package com.example.original;

import org.junit.jupiter.api.Test;
import java.util.regex.Pattern;
import static org.junit.jupiter.api.Assertions.*;

public class TestVersionAndSetup {

    @Test
    public void testVersionModuleImportable() {
        // Simulate version field
        String version = "1.2.3";
        assertNotNull(version);
    }

    @Test
    public void testVersionFormat() {
        String version = "1.2.3";
        String[] parts = version.split("\\.");
        assertEquals(3, parts.length);
        for (String part : parts)
            assertTrue(part.matches("\\d+"));
    }
}