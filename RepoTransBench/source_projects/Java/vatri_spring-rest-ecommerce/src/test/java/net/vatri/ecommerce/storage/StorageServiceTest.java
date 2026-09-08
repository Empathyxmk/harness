package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StorageServiceTest {

    @Test
    void dummyInterfaceImplementation() {
        // Since StorageService is an interface, ensure that it can be implemented
        class MyStorageService implements StorageService {
            public void init() {}
            public String store(org.springframework.web.multipart.MultipartFile f, String s) { return "ok"; }
            public java.util.stream.Stream<java.nio.file.Path> loadAll() { return java.util.stream.Stream.empty(); }
            public java.nio.file.Path load(String file) { return null; }
            public org.springframework.core.io.Resource loadAsResource(String file) { return null; }
            public void deleteAll() {}
        }
        StorageService s = new MyStorageService();
        assertNotNull(s);
        assertDoesNotThrow(s::init);
        assertEquals("ok", s.store(null,""));
        assertNotNull(s.loadAll());
        assertNull(s.load(""));
        assertNull(s.loadAsResource(""));
        assertDoesNotThrow(s::deleteAll);
    }
}