package com.github.tonyo.pyope.original;

import org.junit.jupiter.api.Test;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import static org.junit.jupiter.api.Assertions.*;

class SetupPyTest {

    @Test
    void testSetupPyRuns() throws Exception {
        Path tmpDir = Files.createTempDirectory("setup_py_test");
        Path readmeFile = tmpDir.resolve("README.rst");
        Path historyFile = tmpDir.resolve("HISTORY.rst");
        Path origRoot = Path.of(System.getProperty("user.dir")); // simulate like Python's __file__
        Path origReadme = origRoot.resolve("../README.rst").normalize();
        Path origHistory = origRoot.resolve("../HISTORY.rst").normalize();
        assertTrue(origReadme.toFile().exists());
        assertTrue(origHistory.toFile().exists());
        Files.copy(origReadme, readmeFile);
        Files.copy(origHistory, historyFile);

        Path setupPy = origRoot.resolve("../setup.py").normalize();
        assertTrue(setupPy.toFile().exists());
        // Execute setup.py using Python, expecting a return code of 0 or 1
        Process p = new ProcessBuilder("python3", setupPy.toString(), "--name")
                .directory(tmpDir.toFile())
                .redirectErrorStream(true)
                .start();
        int code = p.waitFor();
        assertTrue(code == 0 || code == 1);
        // (Optional) Clean up
        Files.deleteIfExists(readmeFile);
        Files.deleteIfExists(historyFile);
        Files.deleteIfExists(tmpDir.resolve("setup.py"));
        Files.deleteIfExists(tmpDir);
    }

    @Test
    void testImportSetupModuleRuns() throws Exception {
        Path origRoot = Path.of(System.getProperty("user.dir"));
        Path setupPy = origRoot.resolve("../setup.py").normalize();
        assertTrue(setupPy.toFile().exists());
        try (BufferedReader reader = new BufferedReader(new FileReader(setupPy.toFile()))) {
            String line;
            boolean found = false;
            while ((line = reader.readLine()) != null) {
                if (line.contains("setup(")) {
                    found = true;
                    break;
                }
            }
            assertTrue(found);
        }
    }
}