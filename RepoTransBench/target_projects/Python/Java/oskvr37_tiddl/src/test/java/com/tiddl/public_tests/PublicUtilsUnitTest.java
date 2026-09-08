package com.tiddl.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsUnitTest {

    static class DummyFileUtils {
        static boolean exists = false;
        static boolean fileExists(String f) { return exists; }
    }

    @Test
    void test_file_exists_false() {
        DummyFileUtils.exists = false;
        assertFalse(DummyFileUtils.fileExists("nofile.txt"));
    }

    @Test
    void test_file_exists_true() {
        DummyFileUtils.exists = true;
        assertTrue(DummyFileUtils.fileExists("yes.txt"));
    }
}