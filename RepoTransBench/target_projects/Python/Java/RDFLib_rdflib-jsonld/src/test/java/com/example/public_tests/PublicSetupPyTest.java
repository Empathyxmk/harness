package com.example.public_tests;

import org.junit.jupiter.api.Test;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_setup_py.py
 */
public class PublicSetupPyTest {

    @Test
    public void testSetupRunsWithFakeArgReturnsError() throws Exception {
        String pythonExe = System.getenv("PYTHON") != null ? System.getenv("PYTHON") : "python3";
        String setupPath = Paths.get("setup.py").toAbsolutePath().toString();

        ProcessBuilder pb = new ProcessBuilder(pythonExe, setupPath, "--foobar123");
        pb.redirectErrorStream(true);
        Process process = pb.start();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        InputStream is = process.getInputStream();
        byte[] buf = new byte[1024];
        int n;
        while ((n = is.read(buf)) != -1) {
            baos.write(buf, 0, n);
        }
        int code = process.waitFor();
        String output = baos.toString();
        assertNotEquals(0, code, "Non-zero exit expected for fake argument");
        assertFalse(output.isEmpty(), "Stdout or stderr should contain output");
    }

    @Test
    public void testSetupPyFileExistsAndHasCode() throws IOException {
        String setupPyPath = Paths.get("setup.py").toAbsolutePath().toString();
        assertTrue(Files.exists(Paths.get(setupPyPath)), "setup.py file does not exist");
        String contents = new String(Files.readAllBytes(Paths.get(setupPyPath)));
        assertTrue(
                contents.contains("setup(") ||
                contents.contains("def ") ||
                contents.contains("import ") ||
                contents.contains("class "),
                "setup.py should have code artifacts like 'setup(', 'def ', 'import ', or 'class '"
        );
    }
}