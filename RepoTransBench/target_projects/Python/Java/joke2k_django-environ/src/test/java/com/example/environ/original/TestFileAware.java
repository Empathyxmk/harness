package com.example.environ.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from: tests/test_fileaware.py
 * Note: This code expects that the FileAwareMapping implementation for Java exists 
 *       and mirrors the behavior of the Python version.
 */
public class TestFileAware {
    private FileAwareMapping mapping;

    @BeforeEach
    void setUp(@TempDir Path tempDir) throws Exception {
        // Simulate loading environment variable via file system as done in Django Environ
        Path fooFile = tempDir.resolve("foo.txt");
        Files.write(fooFile, "bar".getBytes());

        // This would be equivalent to env = environ.Env() and env.read_env(...)
        // For Java, you need a FileAwareMapping which supports loading by file reference
        mapping = new FileAwareMapping(Map.of(
            "FOO_FILE", fooFile.toString()
        ));

        // After construction, mapping should have loaded "FOO" key with value "bar"
    }

    @Test
    void testFileValueRead() {
        assertTrue(mapping.containsKey("FOO"));
        assertEquals("bar", mapping.get("FOO"));
    }

    @Test
    void testFallbackToOriginalValueIfNoFile() {
        // If there is a variable without _FILE, we should get that value
        mapping = new FileAwareMapping(Map.of(
            "FOO", "plainbar"
        ));
        assertEquals("plainbar", mapping.get("FOO"));
    }

    @Test
    void testFileKeyOverridesDirectValue(@TempDir Path tempDir) throws Exception {
        // _FILE takes precedence over direct variable
        Path fooFile = tempDir.resolve("foo.txt");
        Files.write(fooFile, "fromfile".getBytes());

        mapping = new FileAwareMapping(Map.of(
            "FOO", "fromenv",
            "FOO_FILE", fooFile.toString()
        ));

        assertEquals("fromfile", mapping.get("FOO"));
    }

    @Test
    void testMissingFileRaisesException(@TempDir Path tempDir) {
        // If _FILE points to a missing file, it should raise IllegalStateException
        Path missingPath = tempDir.resolve("nofile.txt");

        mapping = new FileAwareMapping(Map.of(
            "FOO_FILE", missingPath.toString()
        ));

        assertThrows(IllegalStateException.class, () -> {
            mapping.get("FOO");
        });
    }

    @Test
    void testKeyNotPresentReturnsNull() {
        // If variable is simply not present, should return null (or default if supported)
        mapping = new FileAwareMapping(Map.of());
        assertNull(mapping.get("SOMETHING"));
    }
}