package com.vijos.jd4.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.concurrent.atomic.AtomicBoolean;

class TestCache {

    // Placeholder for the actual cache logic. Adapt as needed for actual Java implementation.
    static class DummyCache {
        static byte[] fileData;

        static InputStream cacheOpen(Object session, String domainId, String pid) throws IOException {
            if (fileData != null) {
                return new ByteArrayInputStream(fileData);
            }
            if (session instanceof DummySession) {
                ((DummySession) session).called.set(true);
                return new ByteArrayInputStream("probdata".getBytes());
            }
            return null;
        }

        static void cacheInvalidate(String domainId, String pid) {
            fileData = null;
        }
    }

    static class DummySession {
        AtomicBoolean called = new AtomicBoolean(false);
    }

    Path tempDir;

    @BeforeEach
    void setup() throws IOException {
        tempDir = Files.createTempDirectory("testcache");
    }

    @AfterEach
    void cleanup() throws IOException {
        if (tempDir != null && Files.exists(tempDir)) {
            Files.walk(tempDir)
                    .sorted((a, b) -> b.compareTo(a))
                    .map(Path::toFile)
                    .forEach(File::delete);
        }
        DummyCache.fileData = null;
    }

    @Test
    void testCacheOpenFileFound() throws IOException {
        // Simulate the file "exists" case
        DummyCache.fileData = "data".getBytes();
        InputStream is = DummyCache.cacheOpen(null, "dom1", "prob");
        byte[] buf = is.readAllBytes();
        is.close();
        assertArrayEquals("data".getBytes(), buf);
    }

    @Test
    void testCacheOpenDownload() throws IOException {
        // Simulate the missing file, so session's download is called
        DummyCache.fileData = null;
        DummySession session = new DummySession();
        InputStream is = DummyCache.cacheOpen(session, "dom2", "p2");
        byte[] buf = is.readAllBytes();
        is.close();
        assertTrue(session.called.get());
        assertArrayEquals("probdata".getBytes(), buf);
    }

    @Test
    void testCacheInvalidate() throws IOException {
        // Existence and removal: DummyCache.fileData is used so just set/unset
        DummyCache.fileData = "x".getBytes();
        DummyCache.cacheInvalidate("dom3", "pp");
        assertNull(DummyCache.fileData);
        // should not throw if called again
        DummyCache.cacheInvalidate("dom3", "pp");
    }
}