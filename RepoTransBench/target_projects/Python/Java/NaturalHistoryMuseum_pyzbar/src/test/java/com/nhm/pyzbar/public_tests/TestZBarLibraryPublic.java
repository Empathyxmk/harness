package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.zbar_library.ZBarLibrary;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestZBarLibraryPublic {
    @Test
    void testLibFound() {
        Object[] result = ZBarLibrary.load();
        String libname = (String) result[0];
        assertNotNull(libname);
        assertTrue(libname instanceof String);
    }

    @Test
    void testLibEndsWithPlatform() {
        Object[] result = ZBarLibrary.load();
        String libname = (String) result[0];
        assertTrue(libname.endsWith(".so") || libname.endsWith(".dll") || libname.endsWith(".dylib"));
    }

    @Test
    void testSearchPathsIncludeLibrary() {
        java.util.List<String> results = ZBarLibrary.searchPaths();
        boolean found = results.stream().anyMatch(path -> path.contains("zbar"));
        assertTrue(found);
    }
}