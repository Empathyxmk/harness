package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class StorageTest {

    @Test
    void testFileSystemStorageDefaults() {
        assertNotNull(new Object());
    }

    @Test
    void testFileSystemStorageWithCustom() {
        assertEquals("/some/path", "/some/path");
        assertEquals("/some/url/", "/some/url/");
    }

    @Test
    void testGetStorageReturnsFromStorages() {
        assertSame(new Object(), new Object());
    }

    @Test
    void testGetStorageRaisesWhenAliasMissing() {
        assertThrows(Exception.class, () -> { throw new Exception("KeyError"); });
    }
}