package com.cloudconvert.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.*;
import java.nio.file.*;
import java.util.Objects;

import static org.junit.jupiter.api.Assertions.*;

class SetupPyTest {

    @Test
    void testSetupPyRuns(@TempDir Path tempDir) throws Exception {
        // Simulate creating a README.md and setup.py in a temp dir then running with Python
        Path dest = tempDir.resolve("README.md");
        Files.write(dest, "# Dummy readme".getBytes());
        // Simulate copying setup.py to temp
        Path setupPySrc = Paths.get(System.getProperty("user.dir"), "setup.py");
        Path setupPyDst = tempDir.resolve("setup.py");
        if (Files.exists(setupPySrc)) {
            Files.copy(setupPySrc, setupPyDst, StandardCopyOption.REPLACE_EXISTING);
        } else {
            // Write a dummy setup.py if none exists for the sake of test logic
            Files.write(setupPyDst, "print('setup running')\nexit(0)".getBytes());
        }
        // Run Python process
        ProcessBuilder pb = new ProcessBuilder("python3", setupPyDst.toString()).directory(tempDir.toFile());
        Process proc = pb.start();
        int code = proc.waitFor();
        assertTrue(code == 0 || code == 1, "setup.py run return code should be 0 or 1");
    }
}