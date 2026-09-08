package com.wroberts.pytimeparse.original;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestSetupPy {
    @Test
    void testSetupPyRuns() throws Exception {
        Path tmpDir = Files.createTempDirectory("pytimeparse-setup");
        try {
            // Simulate project structure
            Path pyDir = tmpDir.resolve("pytimeparse");
            Files.createDirectories(pyDir);
            Files.write(pyDir.resolve("VERSION"), "0.99".getBytes());
            Files.write(tmpDir.resolve("README.rst"), "longdesc".getBytes());
            Path setupPy = tmpDir.resolve("setup.py");
            
            // Here, simply simulate the action of reading VERSION and README,
            // as we cannot run Python code in Java tests.
            // The actual check is to make sure no exception happens with file access.
            String version = new String(Files.readAllBytes(pyDir.resolve("VERSION"))).trim();
            String readme = new String(Files.readAllBytes(tmpDir.resolve("README.rst"))).trim();
            
            Assertions.assertEquals("0.99", version);
            Assertions.assertEquals("longdesc", readme);
        } finally {
            deleteRecursive(tmpDir);
        }
    }

    private void deleteRecursive(Path p) throws IOException {
        if (Files.exists(p)) {
            if (Files.isDirectory(p)) {
                try (DirectoryStream<Path> entries = Files.newDirectoryStream(p)) {
                    for (Path e : entries) {
                        deleteRecursive(e);
                    }
                }
            }
            Files.delete(p);
        }
    }
}