package com.example.original;

import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

import static org.junit.jupiter.api.Assertions.*;

class TestSetupPy {
    @Test
    void testSetupPyExistsAndHasSetupCall() throws IOException {
        File setup = new File("setup.py");
        assertTrue(setup.exists(), "setup.py should exist");
        String content = Files.readString(setup.toPath());
        assertTrue(content.contains("setup("), "setup.py should contain 'setup('");
        assertTrue(content.contains("__name__"), "setup.py should contain '__name__'");
    }
}