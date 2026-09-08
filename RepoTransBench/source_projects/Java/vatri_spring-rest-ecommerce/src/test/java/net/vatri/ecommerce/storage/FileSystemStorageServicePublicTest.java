package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.springframework.core.io.Resource;
import org.springframework.mock.web.MockMultipartFile;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class FileSystemStorageServicePublicTest {

    private final Path testLocation = Paths.get("test-public-upload-dir");

    @BeforeEach
    void setUp() throws Exception {
        Files.createDirectories(testLocation);
    }

    @AfterEach
    void tearDown() throws Exception {
        // Clean up files after test
        if (Files.exists(testLocation)) {
            try (Stream<Path> walk = Files.walk(testLocation)) {
                walk.sorted((a, b) -> b.compareTo(a)) // Delete from deepest
                        .forEach(path -> {
                            try { Files.deleteIfExists(path); } catch (Exception ignored) {}
                        });
            }
        }
    }

    @Test
    void testStoreAndLoadPublicFile() throws Exception {
        StorageProperties properties = new StorageProperties();
        properties.setLocation("test-public-upload-dir");
        FileSystemStorageService storageService = new FileSystemStorageService(properties);
        storageService.init();
        MockMultipartFile file = new MockMultipartFile("publicfile", "publicfile.txt", "text/plain", "test public content".getBytes());

        String storedFileName = storageService.store(file, "publicfile.txt");
        assertEquals("publicfile.txt", storedFileName);

        Path loadedPath = storageService.load("publicfile.txt");
        assertEquals(testLocation.resolve("publicfile.txt").toAbsolutePath(), loadedPath.toAbsolutePath());

        Resource resource = storageService.loadAsResource("publicfile.txt");
        assertNotNull(resource);
        assertTrue(resource.exists());

        // Test loadAll returns our uploaded file
        boolean found = storageService.loadAll().anyMatch(p -> p.getFileName().toString().equals("publicfile.txt"));
        assertTrue(found);
    }

    @Test
    void testDeleteAllPublic() throws Exception {
        StorageProperties properties = new StorageProperties();
        properties.setLocation("test-public-upload-dir");
        FileSystemStorageService storageService = new FileSystemStorageService(properties);
        storageService.init();

        Files.write(testLocation.resolve("todelete-public.txt"), "dummy".getBytes());
        assertTrue(Files.exists(testLocation.resolve("todelete-public.txt")));
        storageService.deleteAll();
        assertFalse(Files.exists(testLocation.resolve("todelete-public.txt")));
    }
}