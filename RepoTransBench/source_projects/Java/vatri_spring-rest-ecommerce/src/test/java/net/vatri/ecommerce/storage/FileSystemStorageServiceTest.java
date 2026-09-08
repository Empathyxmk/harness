package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.*;
import org.springframework.core.io.Resource;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class FileSystemStorageServiceTest {

    private static final String TEST_LOCATION = "test-uploads";
    private FileSystemStorageService storageService;
    private StorageProperties properties;

    @BeforeAll
    void setup() {
        properties = new StorageProperties();
        properties.setLocation(TEST_LOCATION);
        storageService = new FileSystemStorageService(properties);
        storageService.deleteAll();
        storageService.init();
    }

    @AfterAll
    void cleanup() {
        storageService.deleteAll();
    }

    @Test
    void testInitCreatesDirectory() {
        Path rootPath = Paths.get(TEST_LOCATION);
        assertTrue(Files.exists(rootPath));
        assertTrue(Files.isDirectory(rootPath));
    }

    @Test
    void testStoreValidFile() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
                "file", "test.txt", "text/plain", "Spring Boot".getBytes());
        String path = "subdir";
        String storedName = storageService.store(file, path);

        Path expectedDir = Paths.get(TEST_LOCATION, path);
        assertTrue(Files.exists(expectedDir));
        List<Path> files = Files.list(expectedDir).collect(Collectors.toList());
        assertTrue(files.stream().anyMatch(f -> f.getFileName().toString().equals(storedName)));
    }

    @Test
    void testStoreEmptyFileThrows() {
        MockMultipartFile file = new MockMultipartFile(
                "file", "empty.txt", "text/plain", new byte[0]);
        StorageException ex = assertThrows(StorageException.class,
                () -> storageService.store(file, ""));
        assertTrue(ex.getMessage().contains("Failed to store empty file"));
    }

    @Test
    void testLoadAllListsFiles() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
                "file", "loadall.txt", "text/plain", "Test".getBytes());
        storageService.store(file, "");

        try (Stream<Path> paths = storageService.loadAll()) {
            List<Path> files = paths.collect(Collectors.toList());
            assertTrue(files.size() > 0);
        }
    }

    @Test
    void testLoadReturnsCorrectPath() throws IOException {
        String filename = "myfile.txt";
        Path written = Paths.get(TEST_LOCATION, filename);
        Files.write(written, "hello".getBytes());
        Path loaded = storageService.load(filename);
        assertEquals(written, loaded);
    }

    @Test
    void testLoadAsResourceReturnsResource() throws IOException {
        String filename = "resource.txt";
        Path written = Paths.get(TEST_LOCATION, filename);
        Files.write(written, "hello".getBytes());
        Resource resource = storageService.loadAsResource(filename);
        assertTrue(resource.exists());
        assertTrue(resource.isReadable());
    }

    @Test
    void testLoadAsResourceFileNotFound() {
        String filename = "notexist-" + new Random().nextInt() + ".txt";
        Exception ex = assertThrows(StorageFileNotFoundException.class,
                () -> storageService.loadAsResource(filename));
        assertTrue(ex.getMessage().contains(filename));
    }

    @Test
    void testDeleteAllDeletesDirectory() throws IOException {
        Path filePath = Paths.get(TEST_LOCATION, "toremove.txt");
        Files.write(filePath, "bye".getBytes());
        assertTrue(Files.exists(filePath));
        storageService.deleteAll();
        assertFalse(Files.exists(Paths.get(TEST_LOCATION)));
        // restore for next tests!
        storageService.init();
    }

    @Test
    void testInitIOExceptionThrows() throws IOException {
        FileSystemStorageService faulty;
        StorageProperties sp = new StorageProperties() {
            @Override
            public String getLocation() {
                return "/root/forbidden-" + System.currentTimeMillis();
            }
        };
        faulty = new FileSystemStorageService(sp);
        // try to use forbidden directory, likely to fail on most systems w/o permission
        StorageException ex = assertThrows(StorageException.class, faulty::init);
        assertTrue(ex.getMessage().contains("Could not initialize storage"));
    }

    @Test
    void testStoreIOExceptionThrows() {
        // Mock file that throws IOException on getInputStream()
        MockMultipartFile file = new MockMultipartFile("file", "bad.txt", "text/plain", "fail".getBytes()) {
            @Override
            public boolean isEmpty() {
                return false;
            }
            @Override
            public java.io.InputStream getInputStream() throws IOException {
                throw new IOException("forced");
            }
        };

        StorageException ex = assertThrows(StorageException.class,
                () -> storageService.store(file, "badpath"));
        assertTrue(ex.getMessage().contains("Failed to store file"));
    }

    @Test
    void testLoadAllIOExceptionThrows() {
        FileSystemStorageService badService = new FileSystemStorageService(new StorageProperties() {
            @Override
            public String getLocation() {
                return "/root/forbidden-" + System.currentTimeMillis();
            }
        });
        StorageException ex = assertThrows(StorageException.class, badService::loadAll);
        assertTrue(ex.getMessage().contains("Failed to read stored files"));
    }

    @Test
    void testLoadAsResourceMalformedURL() {
        // create a subclass which returns bad path
        FileSystemStorageService badService = new FileSystemStorageService(properties) {
            @Override
            public Path load(String filename) {
                return Paths.get("\0invalid"); // invalid path
            }
        };
        assertThrows(StorageFileNotFoundException.class, () -> badService.loadAsResource("badfile"));
    }
}