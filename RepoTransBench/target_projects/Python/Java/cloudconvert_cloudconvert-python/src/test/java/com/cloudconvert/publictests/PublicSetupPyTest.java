package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.nio.file.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicSetupPyTest {

    @Test
    void testSetupPy(@TempDir Path tmpDir) throws Exception {
        Path setupPy = tmpDir.resolve("setup.py");
        Files.write(setupPy, "print('public setup')\nexit(0)".getBytes());
        ProcessBuilder pb = new ProcessBuilder("python3", setupPy.toString()).directory(tmpDir.toFile());
        int code = pb.start().waitFor();
        assertTrue(code == 0 || code == 1);
    }
}