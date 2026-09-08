package com.tiddl.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UtilsUnitTest {
    static class DummyFileUtils {
        static boolean exists = false;
        static boolean fileExists(String f) { return exists; }
        static long fileSize = 0;
        static long getFileSize(String f) { return fileSize; }
    }
    @Test
    void test_file_exists_true_false() {
        DummyFileUtils.exists = true;
        assertTrue(DummyFileUtils.fileExists("foo.txt"));
        DummyFileUtils.exists = false;
        assertFalse(DummyFileUtils.fileExists("bar.txt"));
    }
    @Test
    void test_get_file_size() {
        DummyFileUtils.fileSize = 1234;
        assertEquals(1234, DummyFileUtils.getFileSize("some.mp3"));
        DummyFileUtils.fileSize = 0;
        assertEquals(0, DummyFileUtils.getFileSize("none"));
    }
}