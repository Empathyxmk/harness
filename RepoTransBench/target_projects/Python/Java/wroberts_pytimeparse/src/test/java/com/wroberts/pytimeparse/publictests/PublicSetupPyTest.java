package com.wroberts.pytimeparse.publictests;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;

public class PublicSetupPyTest {
    @Test
    void testPublicSetupPyRuns() throws Exception {
        Path tmpDir = Files.createTempDirectory("pytimeparse-public-setup");
        try {
            Path pyDir = tmpDir.resolve("pytimeparse");
            Files.createDirectories(pyDir);
            Files.write(pyDir.resolve("VERSION"), "2.77".getBytes());
            Files.write(tmpDir.resolve("README.rst"), "other longdesc".getBytes());
            Path setupPy = tmpDir.resolve("setup.py");
            String version = new String(Files.readAllBytes(pyDir.resolve("VERSION"))).trim();
            String readme = new String(Files.readAllBytes(tmpDir.resolve("README.rst"))).trim();
            
            Assertions.assertEquals("2.77", version);
            Assertions.assertEquals("other longdesc", readme);
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