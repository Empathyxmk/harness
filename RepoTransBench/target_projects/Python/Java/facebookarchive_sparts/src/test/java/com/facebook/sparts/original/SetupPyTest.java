package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class SetupPyTest {
    @Test
    public void testReadDummy() throws Exception {
        Path tmp = Files.createTempDirectory("sparts_test");
        Path filePath = tmp.resolve("foobar.txt");
        Files.write(filePath, "sparts original\n".getBytes());
        assertEquals("sparts original\n", new String(Files.readAllBytes(filePath)));
        Files.delete(filePath);
        Files.delete(tmp);
    }

    @Test
    public void testExistsDummy() throws Exception {
        Path tmp = Files.createTempDirectory("sparts_test");
        Path filePath = tmp.resolve("exist.txt");
        Files.write(filePath, "exists data".getBytes());
        assertTrue(Files.exists(filePath));
        Files.delete(filePath);
        Files.delete(tmp);
    }
}