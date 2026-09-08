package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestSetupPy {
    @Test
    void testSetupPyExists() {
        java.io.File f = new java.io.File("setup.py");
        assertTrue(f.exists(), "setup.py must exist in project root");
    }
}