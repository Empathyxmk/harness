package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.*;
import java.io.IOException;

public class FileTest {
    @Test
    public void testFileBasicReadWriteDelete() throws IOException {
        Path dir = Files.createTempDirectory("sparts_test");
        Path file = dir.resolve("afile.txt");
        Files.write(file, "data".getBytes());
        assertTrue(Files.exists(file));
        assertEquals("data", new String(Files.readAllBytes(file)));
        Files.delete(file);
        assertFalse(Files.exists(file));
        Files.delete(dir);
    }
}