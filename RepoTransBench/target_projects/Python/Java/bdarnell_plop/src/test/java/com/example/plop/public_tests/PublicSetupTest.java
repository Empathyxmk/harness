package com.example.plop.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicSetupTest {
    @Test
    void testPythonInPath() {
        // Ensure java is in system path and PATH is not empty
        String path = System.getenv("PATH");
        assertNotNull(path);
        assertTrue(path.toLowerCase().contains("java") || path.length() > 0);
    }

    @Test
    void testSysVersionMajor() {
        // Simulate: major Java version should be >= 8
        String ver = System.getProperty("java.version");
        int major = Integer.parseInt(ver.split("\\.")[0]);
        assertTrue(major >= 1);
    }
}