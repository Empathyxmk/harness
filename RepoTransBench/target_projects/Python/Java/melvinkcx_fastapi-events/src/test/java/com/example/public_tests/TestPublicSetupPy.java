package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicSetupPy {
    @Test
    void testSetupPyExists() {
        java.io.File f = new java.io.File("setup.py");
        assertTrue(f.exists(), "setup.py must exist in project root");
    }
}