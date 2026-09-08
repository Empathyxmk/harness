package com.ecmwf.ai_models.public_tests;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

class PublicCheckpointTest {

    private static final String SERIAL_FILE = "cpoint_pub.pt";
    static void saveCheckpoint(Map<String, Object> obj, Path path) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(Files.newOutputStream(path))) {
            oos.writeObject(obj);
        }
    }

    static Map<String, Object> loadCheckpoint(Path path) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(Files.newInputStream(path))) {
            return (Map<String, Object>) ois.readObject();
        }
    }

    @Test
    void test_public_checkpoint_create_and_load(@TempDir Path tmpPath) throws IOException, ClassNotFoundException {
        Map<String, Object> data = new HashMap<>();
        data.put("epoch", 7);
        data.put("val_loss", 0.024);
        Path filePath = tmpPath.resolve(SERIAL_FILE);
        saveCheckpoint(data, filePath);
        Map<String, Object> loaded = loadCheckpoint(filePath);
        Assertions.assertEquals(7, loaded.get("epoch"));
        Assertions.assertEquals(0.024, (double) loaded.get("val_loss"), 1e-9);
        Assertions.assertNotEquals(Map.of("epoch", 10, "val_loss", 0.01), loaded);
    }
}