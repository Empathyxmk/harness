package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.Files;
import java.nio.file.Path;

public class FileutilsTest {
    @Test
    public void testFileutilsWriteAndRead() throws Exception {
        Path tmp = Files.createTempDirectory("sparts_test");
        Path filePath = tmp.resolve("fileutils_dummy.txt");
        Files.write(filePath, "some fileutils\n".getBytes());
        assertEquals("some fileutils\n", new String(Files.readAllBytes(filePath)));
        Files.delete(filePath);
        Files.delete(tmp);
    }
}