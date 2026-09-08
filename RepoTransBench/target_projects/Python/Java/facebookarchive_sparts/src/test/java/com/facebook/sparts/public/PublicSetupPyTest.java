package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class PublicSetupPyTest {
    @Test
    public void testPublicReadDummy() throws Exception {
        Path tmp = Files.createTempDirectory("sparts_test");
        Path filePath = tmp.resolve("defabc.txt");
        Files.write(filePath, "sparts test\n".getBytes());
        assertEquals("sparts test\n", new String(Files.readAllBytes(filePath)));
        Files.delete(filePath);
        Files.delete(tmp);
    }

    @Test
    public void testPublicExistsDummy() throws Exception {
        Path tmp = Files.createTempDirectory("sparts_test");
        Path filePath = tmp.resolve("another.txt");
        Files.write(filePath, "hello world".getBytes());
        assertTrue(Files.exists(filePath));
        Files.delete(filePath);
        Files.delete(tmp);
    }
}