package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.File;

public class TestPublicSetup {

    @Test
    public void testPublicSetupPyRuns() {
        File f = new File("setup.py");
        assertTrue(f.exists() && f.isFile());
    }
}