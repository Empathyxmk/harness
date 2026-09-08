package com.example.environ.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class TestFileAwareMappingUnit {

    @Test
    void testConstructWithFile(@TempDir Path tempDir) throws Exception {
        Path file = tempDir.resolve("DATA.txt");
        Files.write(file, "datavalue".getBytes());
        FileAwareMapping mapping = new FileAwareMapping(Map.of(
            "DATA_FILE", file.toString()
        ));
        assertEquals("datavalue", mapping.get("DATA"));
    }

    @Test
    void testConstructWithoutFile() {
        FileAwareMapping mapping = new FileAwareMapping(Map.of(
            "OTHER", "plain"
        ));
        assertEquals("plain", mapping.get("OTHER"));
        assertNull(mapping.get("MISSING"));
    }

    @Test
    void testFileAndEnvValuePriority(@TempDir Path tempDir) throws Exception {
        Path file = tempDir.resolve("DATA.txt");
        Files.write(file, "fromfile".getBytes());
        FileAwareMapping mapping = new FileAwareMapping(Map.of(
            "DATA", "fromenv",
            "DATA_FILE", file.toString()
        ));
        assertEquals("fromfile", mapping.get("DATA"));
    }

    @Test
    void testMissingFileThrows(@TempDir Path tempDir) {
        Path file = tempDir.resolve("xxx.txt");
        FileAwareMapping mapping = new FileAwareMapping(Map.of(
            "DATA_FILE", file.toString()
        ));
        assertThrows(IllegalStateException.class, () -> mapping.get("DATA"));
    }
}