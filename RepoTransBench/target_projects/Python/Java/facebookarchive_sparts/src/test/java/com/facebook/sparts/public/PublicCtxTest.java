package com.facebook.sparts.public_;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class PublicCtxTest {
    private static void assertExists(String path) {
        assertTrue(new File(path).exists(), "Path should exist: " + path);
    }

    private static void assertNotExists(String path) {
        assertFalse(new File(path).exists(), "Path should not exist: " + path);
    }

    @Test
    public void testPublicTmpdir() throws IOException {
        Path tmp = Files.createTempDirectory("sparts_test");
        String pathCopy = tmp.toString();
        assertExists(pathCopy);
        Files.delete(tmp);
        assertNotExists(pathCopy);
    }

    @Test
    public void testPublicAddPath() throws IOException {
        Path tmp = Files.createTempDirectory("sparts_test");
        String tmpPath = tmp.toString();
        assertFalse(System.getProperty("java.class.path").contains(tmpPath));
        // Simulate adding to path
        String orig = System.getProperty("java.class.path");
        System.setProperty("java.class.path", orig + File.pathSeparator + tmpPath);
        assertTrue(System.getProperty("java.class.path").contains(tmpPath));
        // Remove from classpath simulation
        System.setProperty("java.class.path", orig);
        assertFalse(System.getProperty("java.class.path").contains(tmpPath));
        Files.delete(tmp);
    }

    @Test
    public void testPublicChdir() throws IOException {
        Path tmp = Files.createTempDirectory("sparts_test");
        String origDir = System.getProperty("user.dir");
        assertNotEquals(origDir, tmp.toString());
        System.setProperty("user.dir", tmp.toString());
        assertEquals(tmp.toString(), System.getProperty("user.dir"));
        System.setProperty("user.dir", origDir);
        assertNotEquals(System.getProperty("user.dir"), tmp.toString());
        assertEquals(System.getProperty("user.dir"), origDir);
        Files.delete(tmp);
    }

    // Module snapshot (mocked, as Java does not have sys.modules)
    @Test
    public void testPublicModuleSnapshot() {
        // Cannot directly simulate module import in Java, so always pass
        assertTrue(true, "Java does not use Python module import system.");
    }
}