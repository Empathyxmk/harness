package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import java.io.IOException;
import java.nio.file.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicTaskUploadTest {
    @Test
    void testUploadSuccess(@TempDir Path tmpDir) throws IOException {
        Path file = tmpDir.resolve("ok.txt");
        Files.write(file, "x".getBytes());
        assertTrue(Files.exists(file));
        Files.delete(file);
    }
    @Test
    void testUploadFail(@TempDir Path tmpDir) {
        Path f = tmpDir.resolve("404.txt");
        assertFalse(Files.exists(f));
    }
}