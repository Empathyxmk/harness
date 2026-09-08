package com.vijos.jd4.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.util.concurrent.atomic.AtomicBoolean;

class PublicCacheTest {

    static class DummyCache {
        static byte[] fileData;

        static InputStream cacheOpen(Object session, String domainId, String pid) throws IOException {
            if (fileData != null) {
                return new ByteArrayInputStream(fileData);
            }
            if (session instanceof DummySessionPub) {
                ((DummySessionPub) session).called.set(true);
                return new ByteArrayInputStream("pubprobdata".getBytes());
            }
            return null;
        }

        static void cacheInvalidate(String domainId, String pid) {
            fileData = null;
        }
    }

    static class DummySessionPub {
        AtomicBoolean called = new AtomicBoolean(false);
    }

    @Test
    void testPublicCacheOpenFileFound() throws IOException {
        DummyCache.fileData = "newdata".getBytes();
        InputStream is = DummyCache.cacheOpen(null, "domX", "probz");
        byte[] buf = is.readAllBytes();
        is.close();
        assertArrayEquals("newdata".getBytes(), buf);
    }

    @Test
    void testPublicCacheOpenDownload() throws IOException {
        DummyCache.fileData = null;
        DummySessionPub session = new DummySessionPub();
        InputStream is = DummyCache.cacheOpen(session, "domY", "pz0");
        byte[] buf = is.readAllBytes();
        is.close();
        assertTrue(session.called.get());
        assertArrayEquals("pubprobdata".getBytes(), buf);
    }

    @Test
    void testPublicCacheInvalidate() throws IOException {
        DummyCache.fileData = "z".getBytes();
        DummyCache.cacheInvalidate("domZ", "ppq");
        assertNull(DummyCache.fileData);
        // Should not throw if called again
        DummyCache.cacheInvalidate("domZ", "ppq");
    }
}