package com.example.public_tests;

import org.junit.jupiter.api.Test;

import java.io.File;
import java.nio.file.Files;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicSetupPy {
    @Test
    void testPublicVersionExists() throws Exception {
        File setupPy = new File("setup.py");
        assertTrue(setupPy.exists(), "setup.py must exist");
        String content = Files.readString(setupPy.toPath());
        assertTrue(content.contains("version"), "setup.py must contain 'version'");
    }

    @Test
    void testPublicDescriptionExists() throws Exception {
        File setupPy = new File("setup.py");
        assertTrue(setupPy.exists(), "setup.py must exist");
        String content = Files.readString(setupPy.toPath());
        assertTrue(content.contains("description"), "setup.py must contain 'description'");
    }
}