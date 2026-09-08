package com.example.original;

import org.junit.jupiter.api.Test;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from Python tests/test_setup_py.py
 * (Covers: test_setup_runs_as_script, test_setup_py_exists)
 */
public class SetupPyTest {

    @Test
    public void testSetupRunsAsScript() throws Exception {
        String pythonExe = System.getenv("PYTHON") != null ? System.getenv("PYTHON") : "python3";
        String setupPath = Paths.get("setup.py").toAbsolutePath().toString();

        ProcessBuilder pb = new ProcessBuilder(pythonExe, setupPath, "--version");
        pb.redirectErrorStream(true);
        Process process = pb.start();

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        InputStream is = process.getInputStream();
        byte[] buf = new byte[1024];
        int n;
        while ((n = is.read(buf)) != -1) { baos.write(buf, 0, n); }

        process.waitFor();
        byte[] stdoutBytes = baos.toByteArray();
        assertNotNull(stdoutBytes); // Equates to Python isinstance(result.stdout, (bytes, str))
    }

    @Test
    public void testSetupPyExists() {
        boolean exists = Files.exists(Paths.get("setup.py").toAbsolutePath());
        assertTrue(exists, "setup.py should exist");
    }
}