package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StorageServicePublicTest {

    @Test
    void dummyInterfaceImplementationDifferentData() {
        // Provide a different return for store, different input for load
        class MyStorageService implements StorageService {
            public void init() {}
            public String store(org.springframework.web.multipart.MultipartFile f, String s) { return "public-ok"; }
            public java.util.stream.Stream<java.nio.file.Path> loadAll() { return java.util.stream.Stream.of(java.nio.file.Paths.get("publicfile")); }
            public java.nio.file.Path load(String file) { return java.nio.file.Paths.get("publicfile"); }
            public org.springframework.core.io.Resource loadAsResource(String file) { return null; }
            public void deleteAll() {}
        }
        StorageService s = new MyStorageService();
        assertNotNull(s);
        assertDoesNotThrow(s::init);
        assertEquals("public-ok", s.store(null,"public"));
        assertTrue(s.loadAll().findFirst().isPresent());
        assertEquals(java.nio.file.Paths.get("publicfile"), s.load("public"));
        assertNull(s.loadAsResource("public"));
        assertDoesNotThrow(s::deleteAll);
    }
}